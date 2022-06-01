from http import HTTPStatus

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from api.v1.pagination import PaginatedParams
from core.decorators import cache
from models.response_models import GenreAPI
from services.common import RetrivalService
from services.genres import get_genre_service

from .exceptions import GenreExceptionMessages as GEM

router = APIRouter()


@router.get(
    "/",
    response_model=list[GenreAPI],
    summary="все жанры",
    description="Постраничный вывод жанров",
    response_description="Название и описание жанра",
)
@cache()
async def get_genres(
    page_param: PaginatedParams = Depends(),
    genre_service: RetrivalService = Depends(get_genre_service),
) -> list[GenreAPI]:
    genres = await genre_service.get_by_query(size=page_param.page_size, from_=page_param.get_starting_doc())
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GEM.GENRES_NOT_FOUND)
    return [GenreAPI(**genre.get_api_fields()) for genre in genres]


@router.get(
    "/{uuid}",
    response_model=GenreAPI,
    summary="жанр по uuid",
    description="Поиск жанра по идентификатору",
    response_description="Название и описание жанра",
)
async def genre_details(
    uuid: str,
    genre_services: RetrivalService = Depends(get_genre_service),
) -> GenreAPI:
    genre = await genre_services.get_by_id(uuid)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GEM.GENRE_NOT_FOUND)
    return GenreAPI(**genre.get_api_fields())
