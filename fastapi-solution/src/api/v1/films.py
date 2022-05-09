from http import HTTPStatus
from typing import Optional

from api.v1.queries import get_query_film_by_genre, get_query_film_search
from api.v1.pagination import PaginatedParams
from core.decorators import cache
from .exceptions import FilmExceptionMessages as FEM
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Query
from fastapi.routing import APIRouter
from models.response_models import FilmAPI, ShortFilmAPI
from services.common import RetrivalService
from services.films import get_film_service, get_short_film_service

router = APIRouter()


@router.get(
    '/', 
    response_model=list[ShortFilmAPI],
    summary="все фильмы",
    description="Вывод всех популярных кинопроизведений",
    response_description="Название и рейтинг фильма",
)
@cache()
async def popular_films(
    page_param: PaginatedParams = Depends(),
    sort: str = Query('-imdb_rating', regex="^-imdb_rating$|^imdb_rating$"),
    genre: Optional[str] = None,
    film_service: RetrivalService = Depends(get_short_film_service),
) -> list[ShortFilmAPI]:
    films = await film_service.get_by_query(
        sort=sort, size=page_param.page_size, from_=page_param.get_starting_doc(), **get_query_film_by_genre(genre),
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FEM.FILMS_NOT_FOUND)
    return [ShortFilmAPI(**film.get_api_fields()) for film in films]


@router.get(
    '/{uuid}', 
    response_model=FilmAPI,
    summary="Фильм по uuid",
    description="Запрос фильма по его идентификатору",
    response_description="Полная информация о фильме",
)
async def film_details(
    uuid: str,
    film_service: RetrivalService = Depends(get_film_service),
) -> FilmAPI:
    film = await film_service.get_by_id(uuid)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FEM.FILM_NOT_FOUND)
    return FilmAPI(**film.get_api_fields())


@router.get(
    '/search/',
    response_model=list[ShortFilmAPI],
    summary="поиск фильма",
    description="Полнотекстовый поиск по кинопроизведениям",
    response_description="Название и рейтинг фильма",
)
@cache()
async def films_search(
    query: str,
    page_param: PaginatedParams = Depends(),
    film_service: RetrivalService = Depends(get_short_film_service),
) -> list[ShortFilmAPI]:
    films = await film_service.get_by_query(
        size=page_param.page_size, from_=page_param.get_starting_doc(), **get_query_film_search(query),
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FEM.FILMS_NOT_FOUND)
    return [ShortFilmAPI(**film.get_api_fields()) for film in films]
