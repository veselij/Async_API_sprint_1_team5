from typing import Optional

from pydantic import BaseModel

from .common import ConfigMixin


class FilmAPI(BaseModel, ConfigMixin):
    uuid: str
    title: str
    imdb_rating: float
    description: Optional[str]
    genre: Optional[list[dict[str, str]]]
    actors: Optional[list[dict[str, str]]]
    writers: Optional[list[dict[str, str]]]
    directors: Optional[list[dict[str, str]]]
    subscription: Optional[list[dict[str, str]]]


class ShortFilmAPI(BaseModel, ConfigMixin):
    uuid: str
    title: str
    imdb_rating: float


class GenreAPI(BaseModel, ConfigMixin):
    uuid: str
    name: str
    description: Optional[str]


class PersonAPI(BaseModel, ConfigMixin):
    uuid: str
    full_name: str
    role: str
    film_ids: Optional[list[str]]
