from typing import Type

from elastic_transport import ConnectionError
from elasticsearch import AsyncElasticsearch

es: AsyncElasticsearch


async def get_elastic() -> tuple[AsyncElasticsearch, Type[Exception]]:
    return es, ConnectionError
