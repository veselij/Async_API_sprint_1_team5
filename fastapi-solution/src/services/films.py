from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi.param_functions import Depends
from functools import lru_cache

from common import RetrivalService
from db.elastic import get_elastic
from db.redis import get_redis
from models.common import Film


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> RetrivalService:
    return RetrivalService(redis, elastic, Film, 'movies')

