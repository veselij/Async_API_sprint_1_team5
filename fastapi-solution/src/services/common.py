from abc import ABC, abstractmethod
from typing import Optional, Type

from aioredis import Redis
import aioredis
import backoff
import elasticsearch.exceptions as es_exceptions
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from models.common import BaseModel


class DataBaseManager(ABC):

    @abstractmethod
    async def get_obj_from_db_by_id(self, obj_id: str, table_name: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def get_objs_by_query(self, table_name: str, **kwargs) -> Optional[list[dict]]:
        pass


class ElasticDataBaseManager(DataBaseManager):

    def __init__(self, elastic: AsyncElasticsearch) -> None:
        self.elastic = elastic

    @backoff.on_exception(backoff.expo, (es_exceptions.ConnectionTimeout, es_exceptions.ConnectionError), max_tries=3)
    async def get_obj_from_db_by_id(self, obj_id: str, table_name: str) -> Optional[dict]:
        try:
            doc = await self.elastic.get(index=table_name, id=obj_id)
        except NotFoundError:
            return None
        return doc['_source']

    @backoff.on_exception(backoff.expo, (es_exceptions.ConnectionTimeout, es_exceptions.ConnectionError), max_tries=3)
    async def get_objs_by_query(self, table_name: str, **kwargs) -> Optional[list[dict]]:
        if kwargs.get('sort', None) is not None and kwargs['sort'].startswith('-'):
            kwargs['sort'] = "{0}:desc".format(kwargs['sort'][1:])
        try:
            docs = await self.elastic.search(index=table_name, **kwargs)
        except NotFoundError:
            return None
        return [fields['_source'] for fields in docs['hits']['hits']]


class BaseCache(ABC):

    cache_timer = 60 * 5

    @abstractmethod
    async def get_obj_from_cache(self, obj_id: str) -> Optional[str]:
        pass

    @abstractmethod
    async def put_obj_to_cache(self, key: str, obj: str) -> None:
        pass


class RedisCache(BaseCache):

    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    @backoff.on_exception(backoff.expo, (aioredis.ConnectionClosedError), max_tries=3)
    async def get_obj_from_cache(self, obj_id: str) -> Optional[str]:
        data = await self.redis.get(obj_id)
        if not data:
            return None
        return data

    @backoff.on_exception(backoff.expo, (aioredis.ConnectionClosedError), max_tries=3)
    async def put_obj_to_cache(self, key: str, obj: str) -> None:
        await self.redis.set(key, obj, expire=self.cache_timer)


class RetrivalService:

    def __init__(self, cache: BaseCache, db_manager: DataBaseManager, base_obj: Type[BaseModel], index_name: str):
        self.cache = cache
        self.db_manager = db_manager
        self.base_obj = base_obj
        self.index_name = index_name

    async def get_by_id(self, obj_id: str) -> Optional[BaseModel]:
        obj = await self.cache.get_obj_from_cache(obj_id)
        if not obj:
            obj = await self.db_manager.get_obj_from_db_by_id(obj_id, self.index_name)
            if not obj:
                return None
            obj_model = self.base_obj.parse_obj(obj)
            await self.cache.put_obj_to_cache(obj_model.uuid, obj_model.json())
        else:
            obj_model = self.base_obj.parse_raw(obj)
        return obj_model

    async def get_by_query(self, **kwargs) -> Optional[list[BaseModel]]:
        docs = await self.db_manager.get_objs_by_query(self.index_name, **kwargs)
        if not docs:
            return None
        return [self.base_obj.parse_obj(fields) for fields in docs]
