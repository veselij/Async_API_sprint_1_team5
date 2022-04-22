from http import HTTPStatus

from core.decorators import cache
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from exceptions import GenreExceptionMessages as GEM
from models.response_models import GenreAPI
from services.common import RetrivalService
from services.genres import get_genre_service

router = APIRouter()


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
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GEM.GENRES_NOT_FOUND)
    return [GenreAPI(**genre.get_api_fields()) for genre in genres]


@router.get('/{uuid}', response_model=GenreAPI)
@cache()
async def genre_details(
    uuid: str, genre_services: RetrivalService = Depends(get_genre_service),
) -> GenreAPI:
    genre = await genre_services.get_by_id(uuid)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GEM.GENRE_NOT_FOUND)
    return GenreAPI(**genre.get_api_fields())
