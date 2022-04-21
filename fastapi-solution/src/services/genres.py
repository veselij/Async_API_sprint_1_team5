from functools import lru_cache

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi.param_functions import Depends
from models.common import Genre

from services.common import RetrivalService


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> RetrivalService:
    return RetrivalService(redis, elastic, Genre, 'genres')
