from typing import Type
from elasticsearch import AsyncElasticsearch
from elastic_transport import ConnectionError

es: AsyncElasticsearch


async def get_elastic() -> tuple[AsyncElasticsearch, Type[Exception]]:
    return es, ConnectionError
