from typing import Optional
from .common import ConfigMixin
from pydantic import BaseModel


class FilmAPI(BaseModel, ConfigMixin):
    title: str
    imdb_rating: float
    description: Optional[str]
    genre: Optional[list[dict[str, str]]]
    actors: Optional[list[dict[str, str]]]
    writers: Optional[list[dict[str, str]]]
    directors: Optional[list[dict[str, str]]]


class ShortFilmAPI(BaseModel, ConfigMixin):
    title: str
    imdb_rating: str


class GenreAPI(BaseModel, ConfigMixin):
    name: str
    description: Optional[str]


class PersonAPI(BaseModel, ConfigMixin):
    full_name: str
    role: str
    film_ids: Optional[list[str]]
    