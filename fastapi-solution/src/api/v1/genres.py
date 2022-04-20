from http import HTTPStatus

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from pydantic import BaseModel

from services.common import RetrivalService
from services.genres import get_genre_service

router = APIRouter()


class Genre(BaseModel):
    id: str
    name: str
    description: str


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, genre_services: RetrivalService = Depends(get_genre_service)) -> Genre:
    genre = await genre_services.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return Genre(**genre.get_api_fields())
