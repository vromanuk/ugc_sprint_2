import os
from functools import lru_cache
from logging import config as logging_config

from pydantic import BaseSettings

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class ClickhouseConfig(BaseSettings):
    CLICKHOUSE_DB_NAME: str = "movies_db"
    CLICKHOUSE_EVENT_TABLE: str = "events"
    CLICKHOUSE_PORT: int = 9000
    CLICKHOUSE_HOST: str = "clickhouse"


class Settings(BaseSettings):
    PROJECT_NAME: str = "ugc"
    LOG_LEVEL: str = "debug"
    API_PREFIX: str = "/api/v1"

    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    clickhouse_config: ClickhouseConfig = ClickhouseConfig()

    FAUST_PROJECT_NAME: str = "movie_progress"
    DEFAULT_NUMBER_PARTITIONS: int = 3
    KAFKA_PORT: int = 9092
    KAFKA_HOST: str = "kafka"


@lru_cache()
def get_settings():
    return Settings(_env_file=".env", _env_file_encoding="utf-8")
