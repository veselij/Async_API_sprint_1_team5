<<<<<<< HEAD
from uuid import UUID
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.films import FilmService, get_film_service
=======
from http import HTTPStatus

from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from pydantic import BaseModel

from services.films import RetrivalService, get_genre_service
>>>>>>> origin/07_genre_person_logic

router = APIRouter()


class Genre(BaseModel):
<<<<<<< HEAD
    id: UUID
    name: str
    description: str

=======
    uuid: str
    name: str


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, genre_service: RetrivalService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return Genre(**genre.get_api_fileds()) 
>>>>>>> origin/07_genre_person_logic
