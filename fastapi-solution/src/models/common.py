import orjson
from abc import abstractmethod
from uuid import UUID
from typing import List, Dict

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


class Film(BaseModel):
    title: str
    description: str
    imdb_rating: float
    genre: List[Dict[UUID, str]]
    directors: List[Dict[UUID, str]]
    actors: List[Dict[UUID, str]]
    writers: List[Dict[UUID, str]]

    def get_api_fields(self):
        return {
            'uuid': self.uuid,
            'title': self.title,
            'imdb_rating': self.imdb_rating,
            'genre': self.genre,
            'directors': self.directors,
            'actors': self.actors,
            'writers': self.writers,
        }


class Genre(BaseModel):
    name: str
    description: str

    def get_api_fields(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'description': self.description,
        }


class Person(BaseModel):
    full_name: str
    role: List[str]
    film_ds: List[UUID]

    def get_api_fields(self):
        return {
            'uuid': self.uuid,
            'role': self.role,
            'film_ids': self.film_ds,
        }
