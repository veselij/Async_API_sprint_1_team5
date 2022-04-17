from typing import Optional
import orjson

from pydantic import BaseModel



def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()



class BaseObject(BaseModel):
    id: str

    def get_api_fileds(self) -> dict:
        """Get api fields"""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(BaseObject):
    title: str
    description: str

    def get_api_fileds(self) -> dict:
        return {'uuid': self.id, 'title': self.title}


class Genre(BaseObject):
    name: str
    description: Optional[str]

    def get_api_fileds(self) -> dict:
        return {'uuid': self.id, 'name': self.name}
    
