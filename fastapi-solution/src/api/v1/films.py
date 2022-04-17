from http import HTTPStatus
from typing import List, Dict
from uuid import UUID

from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from pydantic import BaseModel

from services.films import FilmService
from services.films import get_film_service
router = APIRouter()


class Film(BaseModel):
    title: str
    description: str
    imdb_rating: float
    genre: List[Dict[UUID, str]]
    directors: List[Dict[UUID, str]]
    actors: List[Dict[UUID, str]]
    writers: List[Dict[UUID, str]]


@router.get('/{film_id}', response_model=Film)
async def film_details(
    film_id: str,
    similar: bool = False,
    film_service: FilmService = Depends(get_film_service),
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    if similar:
        films = await film_service.get_by_genre(film.genre)
        if not films:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='similar films not found')
        return [Film(**film.get_api_fields()) for film in films]
    return Film(**film.get_api_fileds())
