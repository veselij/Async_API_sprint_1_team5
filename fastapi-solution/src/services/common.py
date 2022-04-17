from typing import Optional, Type

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError

from models.common import BaseModel

CACHE_EXPIRE_IN_SECONDS = 60 * 5


class RetrivalService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, base_obj: Type[BaseModel], index_name: str):
        self.redis = redis
        self.elastic = elastic
        self.base_obj = base_obj
        self.index_name = index_name

    async def get_by_id(self, obj_id: str) -> Optional[BaseModel]:
        obj = await self._obj_from_cache(obj_id)
        if not obj:
            obj = await self._get_obj_from_elastic(obj_id)
            if not obj:
                return None
            await self._put_obj_to_cache(obj)

        return obj

    async def _get_obj_from_elastic(self, obj_id: str) -> Optional[BaseModel]:
        try:
            doc = await self.elastic.get(self.index_name, obj_id)
        except NotFoundError:
            return None
        return self.base_obj(**doc['_source'])

    async def _obj_from_cache(self, obj_id: str) -> Optional[BaseModel]:
        data = await self.redis.get(obj_id)
        if not data:
            return None

        obj = self.base_obj.parse_raw(data)
        return obj

    async def _put_obj_to_cache(self, obj: BaseModel):
        await self.redis.set(obj.id, obj.json(), expire=CACHE_EXPIRE_IN_SECONDS)
