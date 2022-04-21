from http import HTTPStatus
from typing import Optional

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from pydantic import BaseModel

from services.common import RetrivalService
from services.genres import get_genre_service
from core.decorators import cache

router = APIRouter()


class GenreAPI(BaseModel):
    uuid: str
    name: str
    description: Optional[str]


@router.get('/', response_model=list[GenreAPI])
@cache()
async def get_genres(
    page_num: int = 1,
    page_size: int = 50,
    genre_service: RetrivalService = Depends(get_genre_service),
) -> list[GenreAPI]: 
    starting_doc = (page_num - 1) * page_size
    genres = await genre_service.get_by_query(size=page_size, from_=starting_doc)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    return [GenreAPI(**genre.get_api_fields()) for genre in genres]


@router.get('/{uuid}', response_model=GenreAPI)
@cache()
async def genre_details(uuid: str, genre_services: RetrivalService = Depends(get_genre_service)) -> GenreAPI:
    genre = await genre_services.get_by_id(uuid)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return GenreAPI(**genre.get_api_fields())
