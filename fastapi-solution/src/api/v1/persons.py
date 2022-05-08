from http import HTTPStatus

from api.v1.queries import get_query_films_by_person, get_query_person_search
from core.decorators import cache
from .exceptions import PersonExceptionMessages as PEM
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Query
from fastapi.routing import APIRouter
from models.response_models import ShortFilmAPI, PersonAPI
from services.common import RetrivalService
from services.films import get_short_film_service
from services.persons import get_person_service

router = APIRouter()


@router.get(
    '/{uuid}',
    response_model=PersonAPI,
    summary="все персоны",
    description="Поиск персоны по идентификатору",
    response_description="ФИО, роль и фильмы, в которых принимал участие",
)
@cache()
async def person_details(
    uuid: str, person_services: RetrivalService = Depends(get_person_service),
) -> PersonAPI:
    person = await person_services.get_by_id(uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PEM.PERSON_NOT_FOUND)
    return PersonAPI(**person.get_api_fields())


@router.get(
    '/{uuid}/films/',
    response_model=list[ShortFilmAPI],
    summary="фильмы по персоне",
    description="Поиск фильмов в которых принимала участие персона",
    response_description="Название и рейтинг фильма",
)
@cache()
async def person_films(
    query: str,
    page_num: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1),
    film_service: RetrivalService = Depends(get_short_film_service),
) -> list[ShortFilmAPI]:
    starting_doc = (page_num - 1) * page_size
    films = await film_service.get_by_query(
        size=page_size, from_=starting_doc, **get_query_films_by_person(query),
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PEM.PERSON_DOES_NOT_EXIST + ' or ' + PEM.PERSON_DOES_NOT_HAVE_FILMS,
        )
    return [ShortFilmAPI(**film.get_api_fields()) for film in films]


@router.get(
    '/search/',
    response_model=list[PersonAPI],
    summary="поиск персоны",
    description="Полнотекстовый поиск по персонам",
    response_description="ФИО, роль и фильмы, в которых принимала участие",
)
@cache()
async def person_search(
    query: str,
    page_num: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1),
    person_service: RetrivalService = Depends(get_person_service),
) -> list[PersonAPI]:
    starting_doc = (page_num - 1) * page_size
    persons = await person_service.get_by_query(
        size=page_size, from_=starting_doc, **get_query_person_search(query),
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=PEM.PERSON_NOT_FOUND,
        )
    return [PersonAPI(**person.get_api_fields()) for person in persons]
