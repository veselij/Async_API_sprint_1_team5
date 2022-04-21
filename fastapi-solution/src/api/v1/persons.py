from http import HTTPStatus
from typing import Optional

from api.v1.films import ShortFilmAPI
from api.v1.queries import get_query_films_by_person, get_query_person_search
from core.decorators import cache
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from pydantic import BaseModel
from services.common import RetrivalService
from services.films import get_short_film_service
from services.persons import get_person_service

router = APIRouter()


class PersonAPI(BaseModel):
    uuid: str
    full_name: str
    role: str
    film_ids: Optional[list[str]]


@router.get('/{uuid}', response_model=PersonAPI)
@cache()
async def person_details(
    uuid: str, person_services: RetrivalService = Depends(get_person_service),
) -> PersonAPI:
    person = await person_services.get_by_id(uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return PersonAPI(**person.get_api_fields())


@router.get('/{uuid}/films/', response_model=list[ShortFilmAPI])
@cache()
async def person_films(
    query: str,
    page_num: int = 1,
    page_size: int = 50,
    film_service: RetrivalService = Depends(get_short_film_service),
) -> list[ShortFilmAPI]:
    starting_doc = (page_num - 1) * page_size
    films = await film_service.get_by_query(
        size=page_size, from_=starting_doc, **get_query_films_by_person(query),
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='person does not have films or does not exist',
        )
    return [ShortFilmAPI(**film.get_api_fields()) for film in films]


@router.get('/search/')
@cache()
async def person_search(
    query: str,
    page_num: int = 1,
    page_size: int = 50,
    person_service: RetrivalService = Depends(get_person_service),
) -> list[PersonAPI]:
    starting_doc = (page_num - 1) * page_size
    persons = await person_service.get_by_query(
        size=page_size, from_=starting_doc, **get_query_person_search(query),
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='persons not found',
        )
    return [PersonAPI(**person.get_api_fields()) for person in persons]
