from abc import abstractmethod
from typing import Optional

import orjson
from pydantic import BaseModel as PydanticBaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ConfigMixin:
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class BaseModel(PydanticBaseModel, ConfigMixin):

    uuid: str

    @abstractmethod
    def get_api_fields(self) -> dict:
        pass


class Film(BaseModel):

    title: str
    imdb_rating: float
    description: Optional[str]
    genre: Optional[list[dict[str, str]]]
    actors: Optional[list[dict[str, str]]]
    writers: Optional[list[dict[str, str]]]
    directors: Optional[list[dict[str, str]]]
    subscription: Optional[list[dict[str, str]]]

    def get_api_fields(self) -> dict:
        return {
            "uuid": self.uuid,
            "title": self.title,
            "description": self.description,
            "imdb_rating": self.imdb_rating,
            "genre": self.genre,
            "actors": self.actors,
            "writers": self.writers,
            "directors": self.directors,
            "subscription": self.subscription,
        }


class ShortFilm(Film):
    def get_api_fields(self) -> dict:
        return {
            "uuid": self.uuid,
            "title": self.title,
            "imdb_rating": self.imdb_rating,
        }


class Genre(BaseModel):

    name: str
    description: Optional[str]

    def get_api_fields(self) -> dict:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
        }


class Person(BaseModel):

    full_name: str
    role: str
    film_ids: Optional[list[str]]

    def get_api_fields(self) -> dict:
        return {
            "uuid": self.uuid,
            "full_name": self.full_name,
            "role": self.role,
            "film_ids": self.film_ids,
        }
