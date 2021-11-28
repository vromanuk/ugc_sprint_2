import orjson
from pydantic import BaseModel


class Base(BaseModel):
    class Config:  # noqa: WPS306,WPS431,D106
        json_loads = orjson.loads
        json_dumps = orjson.dumps
