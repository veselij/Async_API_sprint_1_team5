from http import HTTPStatus

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Query
from fastapi.routing import APIRouter

from api.v1.pagination import PaginatedParams
from api.v1.queries import get_query_films_by_person, get_query_person_search
from core.decorators import cache
from models.response_models import PersonAPI, ShortFilmAPI
from services.common import RetrivalService
from services.films import get_short_film_service
from services.persons import get_person_service

from .exceptions import PersonExceptionMessages as PEM

router = APIRouter()


@router.get(
    "/{uuid}",
    response_model=PersonAPI,
    summary="все персоны",
    description="Поиск персоны по идентификатору",
    response_description="ФИО, роль и фильмы, в которых принимал участие",
)
async def person_details(
    uuid: str,
    person_services: RetrivalService = Depends(get_person_service),
) -> PersonAPI:
    person = await person_services.get_by_id(uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PEM.PERSON_NOT_FOUND)
    return PersonAPI(**person.get_api_fields())


@router.get(
    "/{uuid}/films/",
    response_model=list[ShortFilmAPI],
    summary="фильмы по персоне",
    description="Поиск фильмов в которых принимала участие персона",
    response_description="Название и рейтинг фильма",
)
@cache()
async def person_films(
    uuid: str,
    page_param: PaginatedParams = Depends(),
    film_service: RetrivalService = Depends(get_short_film_service),
) -> list[ShortFilmAPI]:
    films = await film_service.get_by_query(
        size=page_param.page_size,
        from_=page_param.get_starting_doc(),
        **get_query_films_by_person(uuid),
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PEM.PERSON_DOES_NOT_EXIST + " or " + PEM.PERSON_DOES_NOT_HAVE_FILMS,
        )
    return [ShortFilmAPI(**film.get_api_fields()) for film in films]


@router.get(
    "/search/",
    response_model=list[PersonAPI],
    summary="поиск персоны",
    description="Полнотекстовый поиск по персонам",
    response_description="ФИО, роль и фильмы, в которых принимала участие",
)
@cache()
async def person_search(
    query: str,
    page_param: PaginatedParams = Depends(),
    person_service: RetrivalService = Depends(get_person_service),
) -> list[PersonAPI]:
    persons = await person_service.get_by_query(
        size=page_param.page_size,
        from_=page_param.get_starting_doc(),
        **get_query_person_search(query),
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PEM.PERSON_NOT_FOUND,
        )
    return [PersonAPI(**person.get_api_fields()) for person in persons]
