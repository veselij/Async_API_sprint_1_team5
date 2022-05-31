from abc import ABC, abstractmethod
import logging
from typing import Optional, Type

from models.common import BaseModel
from core.decorators import backoff_async
from core.exceptions import RetryExceptionError


logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh = logging.FileHandler(filename="/var/log/waiters/backoff.log")
fh.setFormatter(formatter)
logger.addHandler(fh)


class AbstractDatabase(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs) -> dict:
        pass

    @abstractmethod
    async def search(self, *args, **kwargs) -> dict:
        pass


class AbstractCache(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs) -> str:
        pass

    @abstractmethod
    async def set(self, *args, **kwargs) -> None:
        pass


class DataBaseManager:
    def __init__(self, db: AbstractDatabase, retry_exception: Type[Exception]) -> None:
        self.db = db
        self.retry_exception = retry_exception

    @backoff_async(logger, start_sleep_time=0.1, factor=2, border_sleep_time=10)
    async def get_obj_from_db_by_id(self, obj_id: str, table_name: str) -> Optional[dict]:
        try:
            doc = await self.db.get(index=table_name, id=obj_id)
        except self.retry_exception:
            raise RetryExceptionError("database not available")

        if "_source" not in doc:
            return None
        return doc["_source"]

    @backoff_async(logger, start_sleep_time=0.1, factor=2, border_sleep_time=10)
    async def get_objs_by_query(self, table_name: str, **kwargs) -> Optional[list[dict]]:
        if kwargs.get("sort", None) is not None and kwargs["sort"].startswith("-"):
            kwargs["sort"] = "{0}:desc".format(kwargs["sort"][1:])
        try:
            docs = await self.db.search(index=table_name, **kwargs)
        except self.retry_exception:
            raise RetryExceptionError("database not available")

        if "hits" not in docs:
            return None
        return [fields["_source"] for fields in docs["hits"]["hits"]]


class Cache:

    cache_timer = 60 * 5

    def __init__(self, cache: AbstractCache, exc: Type[Exception]) -> None:
        self.cache = cache
        self.exc = exc

    @backoff_async(logger, start_sleep_time=0.1, factor=2, border_sleep_time=10)
    async def get_obj_from_cache(self, obj_id: str) -> Optional[str]:
        try:
            data = await self.cache.get(obj_id)
        except self.exc:
            raise RetryExceptionError("cache not available")

        if not data:
            return None
        return data

    @backoff_async(logger, start_sleep_time=0.1, factor=2, border_sleep_time=10)
    async def put_obj_to_cache(self, key: str, obj: str) -> None:
        try:
            await self.cache.set(key, obj, expire=self.cache_timer)
        except self.exc:
            raise RetryExceptionError("cache not available")


class RetrivalService:
    def __init__(self, cache: Cache, db_manager: DataBaseManager, base_obj: Type[BaseModel], index_name: str):
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
