from functools import lru_cache
from typing import Type

from db.elastic import get_elastic
from db.redis import get_redis
from fastapi.param_functions import Depends
from models.common import Person

from services.common import DataBaseManager, Cache, RetrivalService, AbstractCache, AbstractDatabase


@lru_cache()
def get_person_service(
        cache: tuple[AbstractCache, Type[Exception]] = Depends(get_redis),
        db: tuple[AbstractDatabase, Type[Exception]] = Depends(get_elastic),
) -> RetrivalService:
    return RetrivalService(Cache(*cache), DataBaseManager(*db), Person, 'persons')
