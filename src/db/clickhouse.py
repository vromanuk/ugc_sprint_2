import asyncio
import logging
import multiprocessing
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass

import backoff
from clickhouse_driver import Client

from src.core.config import get_settings
from src.db.models import Event

settings = get_settings()
logger = logging.getLogger()


@dataclass
class ClickhouseClient:  # noqa: WPS306
    client: Client = Client(
        host=settings.clickhouse_config.CLICKHOUSE_HOST,
        port=settings.clickhouse_config.CLICKHOUSE_PORT,
    )

    @classmethod
    async def track_movie_progress(
        cls,
        finished_at: int,
        movie_id_user_id: str,
    ) -> None:
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
    def track_event(cls, event: Event) -> None:
        try:  # noqa: WPS229
            cls.client.execute(
                f"INSERT INTO {event._tablename} (finished_at, movie_id_user_id, event_datetime) VALUES",  # noqa: WPS437,E501
                [event.dict()],
            )
            logger.info("ack")
        except Exception as err:
            logger.error(err)
