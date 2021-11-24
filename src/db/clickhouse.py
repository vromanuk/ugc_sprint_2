import asyncio
import logging
import multiprocessing
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass

import backoff as backoff
from clickhouse_driver import Client

from src.db.models import Event
from src.core.config import get_settings


settings = get_settings()
logger = logging.getLogger()


@dataclass
class ClickhouseClient:
    client: Client = Client(
        host=settings.clickhouse_config.CLICKHOUSE_HOST,
        port=settings.clickhouse_config.CLICKHOUSE_PORT)

    @classmethod
    async def track_movie_progress(cls, finished_at: int, movie_id_user_id: str):
        event = Event(finished_at=finished_at, movie_id_user_id=movie_id_user_id)
        with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(executor, cls.track_event, event)

    @classmethod
    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=3,
        jitter=backoff.random_jitter,
    )
    def track_event(cls, event: Event):
        try:
            cls.client.execute(
                f"INSERT INTO {event._tablename} (finished_at, movie_id_user_id, event_datetime) VALUES",
                [event.dict()],
            )
            logger.info("ack")
        except Exception as e:
            logger.error(e)
