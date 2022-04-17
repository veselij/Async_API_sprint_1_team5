from uuid import UUID
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.films import FilmService, get_film_service

router = APIRouter()


class Genre(BaseModel):
    id: UUID
    name: str
    description: str

