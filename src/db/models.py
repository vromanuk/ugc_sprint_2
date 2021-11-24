from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, PrivateAttr

from src.core.config import get_settings

settings = get_settings()


class Event(BaseModel):
    _tablename: str = PrivateAttr(
        default=f"{settings.clickhouse_config.CLICKHOUSE_DB_NAME}.{settings.clickhouse_config.CLICKHOUSE_EVENT_TABLE}"
    )

    finished_at: Optional[int] = 0
    movie_id_user_id: Optional[str] = ""
    event_datetime: dt = dt.now()
