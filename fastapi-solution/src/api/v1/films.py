from http import HTTPStatus

from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from pydantic import BaseModel

from services.films import RetrivalService, get_film_service

router = APIRouter()


class Film(BaseModel):
    uuid: str
    title: str


@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: RetrivalService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return Film(**film.get_api_fileds()) 
