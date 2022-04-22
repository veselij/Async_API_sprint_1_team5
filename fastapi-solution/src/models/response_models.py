from typing import Optional
from .common import BaseModel


class FilmAPI(BaseModel):

    uuid: str
    title: str
    imdb_rating: float
    description: Optional[str]
    genre: Optional[list[dict[str, str]]]
    actors: Optional[list[dict[str, str]]]
    writers: Optional[list[dict[str, str]]]
    directors: Optional[list[dict[str, str]]]


class ShortFilmAPI(BaseModel):
    uuid: str
    title: str
    imdb_rating: str


class GenreAPI(BaseModel):
    uuid: str
    name: str
    description: Optional[str]


class PersonAPI(BaseModel):
    uuid: str
    full_name: str
    role: str
    film_ids: Optional[list[str]]
    