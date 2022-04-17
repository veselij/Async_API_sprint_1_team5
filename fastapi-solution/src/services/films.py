from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi.param_functions import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.common import Film

from common import RetrivalService



@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> RetrivalService:
    return FilmService(redis, elastic, Film, 'movies')

class FilmService(RetrivalService):

    async def get_by_genre(self, genre: str):
        movies = await self._get_movies_by_genre_from_elastic(genre)
        if not movies:
            return None
        return [self.base_obj(**doc) for doc in movies]

    async def _get_movies_by_genre_from_elastic(self, genre: str):
        query = {
            'query': {
                'match': {
                    'genre': genre,
                }
            },
            'collapse':{
                'field': 'uuid',
            }
        }
        try:
            docs = await self.elastic.search(body=query, index=self.index_name)
        except NotFoundError:
            return None
        return docs
