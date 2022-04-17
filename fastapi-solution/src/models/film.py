from typing import Optional
import orjson
from typing import List, Dict
from uuid import UUID

from pydantic import BaseModel



def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()



<<<<<<< HEAD
class Film(BaseModel):
    id: str
    title: str
    description: str
    # imdb_rating: float
    # genre: List[Dict[UUID, str]]
    # directors: List[Dict[UUID, str]]
    # actors: List[Dict[UUID, str]]
    # writers: List[Dict[UUID, str]]    
=======
class BaseObject(BaseModel):
    id: str

    def get_api_fileds(self) -> dict:
        """Get api fields"""
>>>>>>> origin/07_genre_person_logic

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


<<<<<<< HEAD
=======
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
    
>>>>>>> origin/07_genre_person_logic
