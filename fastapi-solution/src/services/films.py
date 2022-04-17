from functools import lru_cache
from typing import Optional, Type

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi.param_functions import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import BaseObject, Film, Genre

CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class RetrivalService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, base_obj: Type[BaseObject], index_name: str):
        self.redis = redis
        self.elastic = elastic
        self.base_obj = base_obj
        self.index_name = index_name

    # get_by_id возвращает объект фильма. Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, obj_id: str) -> Optional[BaseObject]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        obj = await self._obj_from_cache(obj_id)
        if not obj:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            obj = await self._get_obj_from_elastic(obj_id)
            if not obj:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return None
            # Сохраняем фильм  в кеш
            await self._put_obj_to_cache(obj)

        return obj

    async def _get_obj_from_elastic(self, obj_id: str) -> Optional[BaseObject]:
        try:
            doc = await self.elastic.get(self.index_name, obj_id)
        except NotFoundError:
            return None
        return self.base_obj(**doc['_source'])

    async def _obj_from_cache(self, obj_id: str) -> Optional[BaseObject]:
        # Пытаемся получить данные о фильме из кеша, используя команду get
        # https://redis.io/commands/get
        data = await self.redis.get(obj_id)
        if not data:
            return None

        # pydantic предоставляет удобное API для создания объекта моделей из json
        obj = self.base_obj.parse_raw(data)
        return obj

    async def _put_obj_to_cache(self, obj: BaseObject):
        # Сохраняем данные о фильме, используя команду set
        # Выставляем время жизни кеша — 5 минут
        # https://redis.io/commands/set
        # pydantic позволяет сериализовать модель в json
        await self.redis.set(obj.id, obj.json(), expire=CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> RetrivalService:
    return RetrivalService(redis, elastic, Film, 'movies')


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> RetrivalService:
    return RetrivalService(redis, elastic, Genre, 'genres')
