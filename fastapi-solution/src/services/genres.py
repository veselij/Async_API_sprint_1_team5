from functools import lru_cache
from typing import Type

from fastapi.param_functions import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.common import Genre
from services.common import (AbstractCache, AbstractDatabase, Cache,
                             DataBaseManager, RetrivalService)


@lru_cache()
def get_genre_service(
    cache: tuple[AbstractCache, Type[Exception]] = Depends(get_redis),
    db: tuple[AbstractDatabase, Type[Exception]] = Depends(get_elastic),
) -> RetrivalService:
    return RetrivalService(Cache(*cache), DataBaseManager(*db), Genre, "genres")
