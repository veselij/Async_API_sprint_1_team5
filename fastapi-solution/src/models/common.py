from abc import abstractmethod
import orjson
from uuid import UUID

from pydantic import BaseModel as PydanticBaseModel

def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseModel(PydanticBaseModel):
    uuid: UUID

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

    @abstractmethod
    def get_api_fields(self):
        pass