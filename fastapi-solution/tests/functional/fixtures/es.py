import os
import json
import pytest

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from settings import config



@pytest.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts=["http://{0}:{1}".format(config.es_host, config.es_port)])
    yield client
    await client.close()


@pytest.fixture
def populate_index(es_client):
    def generate_data_for_bulk(data: list, index_name: str):
        for row in data:
            yield {
                "_index": index_name,
                "_id": row["uuid"],
                "_source": row,
            }

    async def inner(data_to_load: str):
        with open(data_to_load, "r") as f:
            data = json.load(f)
        await async_bulk(
            client=es_client,
            actions=generate_data_for_bulk(data, os.path.basename(data_to_load).split("_")[0]),
            refresh="wait_for",
        )

    return inner



@pytest.fixture
async def prepare_es_index(es_client):
    name = []

    async def inner(index_file: str):
        with open(index_file, "r") as f:
            index = json.load(f)
        name.append(os.path.basename(index_file).split(".")[0])
        await es_client.options(ignore_status=400).indices.create(index=name[0], **index)

    yield inner

    await es_client.options(ignore_status=[404]).indices.delete(index=name[0])

