from typing import Type
from elasticsearch import Elasticsearch
from elastic_transport import ConnectionError

es: Elasticsearch


async def get_elastic() -> tuple[Elasticsearch, Type[Exception]]:
    return es, ConnectionError
