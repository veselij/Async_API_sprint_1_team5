from http import HTTPStatus
from uuid import UUID
from typing import Dict, List, Optional 

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from pydantic import BaseModel

from services.films import get_film_service
from services.films import FilmService

router = APIRouter()


class Film(BaseModel):
    title: str
    description: str
    imdb_rating: float
    genre: List[Dict[UUID, str]]
    directors: List[Dict[UUID, str]]
    actors: List[Dict[UUID, str]]
    writers: List[Dict[UUID, str]]

class PopularFilm(BaseModel):
    title: str
    imdb_rating: str
    description: str


@router('/', response_model=PopularFilm)
async def popular_films_by_genre(
    filter_genre_uuid: Optional[UUID],
    sort: str = '-imdb_rating',
    page_size: int = 50,
    page_num: int = 1,
    film_service: FilmService = Depends(get_film_service),
) -> List[PopularFilm]:
    query = {
        'from': (page_num-1)*page_size,
        'size': page_size,
        'sort': [{
            'imdb_rating': {
                'order': 'desc',
            }
        }]
    }
    if filter_genre_uuid is not None:
        query['query'] = {
            'bool': {
                'filter': {
                    'term': {'uuid': filter_genre_uuid},
                }
            },
        },
    films = await film_service._get_by_query(query)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')
    return [PopularFilm(**film.get_api_fields_for_popular()) for film in films]


@router.get('/{film_id}', response_model=Film)
async def film_details(
    film_id: str,
    film_service: FilmService = Depends(get_film_service),
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return Film(**film.get_api_fields())


@router.get('/search', response_model=PopularFilm)
async def films_search(
    query: str,
    page_size: int = 50,
    page_num: int = 1,
    film_service: FilmService = Depends(get_film_service),
) -> List[PopularFilm]:
    query = {
        'from': (page_num-1)*page_size,
        'size': page_size,
        'query': {
            'multi_match': {
                'query': query,
                'fields': ['description', 'title'],
            }
        }
    }
    films = await film_service.get_by_query(query)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')
    return [PopularFilm(**film.get_api_fields_for_popular()) for film in films]
