from typing import List

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi.param_functions import Depends
from functools import lru_cache

from common import RetrivalService, CACHE_EXPIRE_IN_SECONDS
from db.elastic import get_elastic
from db.redis import get_redis
from models.common import Film, BaseModel


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> RetrivalService:
    return FilmService(redis, elastic, Film, 'movies')


class FilmService(RetrivalService):
    async def get_by_genre(self, genre: str):
        movies = await self._get_movies_from_cache_by_genre(genre)
        if not movies:
            movies = await self._get_movies_by_genre_from_elastic(genre)
            if not movies:
                return None
            await self._put_movies_to_cache_by_genre(genre, movies)
        return [self.base_obj(**doc) for doc in movies]

    async def _get_movies_by_genre_from_elastic(self, genre: str):
        query = {
            'query': {
                'match': {
                    'genre': genre,
                },
            },
            'collapse': {
                'field': 'uuid',
            },
        }
        try:
            docs = await self.elastic.search(body=query, index=self.index_name)
        except NotFoundError:
            return None
        return docs

    async def _put_movies_to_cache_by_genre(self, genre: str, movies: List[BaseModel]):
        await self.redis.set(genre, [obj.json() for obj in movies], expire=CACHE_EXPIRE_IN_SECONDS)

    async def _get_movies_from_cache_by_genre(self, genre: str):
        data = await self.redis.get(genre)
        if not data:
            return None

        movies = [self.base_obj.parse_raw(movie) for movie in movies]
        return movies
