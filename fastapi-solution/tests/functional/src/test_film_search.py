import os
import sys

import pytest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from settings import ConfigSettings

config = ConfigSettings()


@pytest.mark.asyncio
async def test_films_search_empty(make_get_request):
    response = await make_get_request('http://{0}:8000/api/v1/films/search/?query='.format(config.api_ip))

    assert response.status == 404
    assert response.body == {'detail': 'Films not found'}


@pytest.mark.asyncio
async def test_films_search_one(make_get_request, prepare_es_index, populate_index):

    await prepare_es_index('testdata/movies.json')
    await populate_index('testdata/movies_data.json')

    response = await make_get_request('http://{0}:8000/api/v1/films/search/?query=Star&page_num=1&page_size=1'.format(config.api_ip))

    assert response.status == 200
    assert response.body[0]['uuid'] == '05d7341e-e367-4e2e-acf5-4652a8435f93'


@pytest.mark.asyncio
async def test_films_search_two(make_get_request, prepare_es_index, populate_index):

    await prepare_es_index('testdata/movies.json')
    await populate_index('testdata/movies_data.json')

    response = await make_get_request('http://{0}:8000/api/v1/films/search/?query=Star&page_num=1&page_size=2'.format(config.api_ip))

    assert response.status == 200
    assert len(response.body) == 2


@pytest.mark.asyncio
async def test_films_search_datatypes(make_get_request, prepare_es_index, populate_index):

    await prepare_es_index('testdata/movies.json')
    await populate_index('testdata/movies_data.json')

    response = await make_get_request('http://{0}:8000/api/v1/films/search/?query=Star&page_num=1&page_size=1'.format(config.api_ip))

    assert response.status == 200
    assert isinstance(response.body[0]['uuid'], str)
    assert isinstance(response.body[0]['title'], str)
    assert isinstance(response.body[0]['imdb_rating'], float)


@pytest.mark.asyncio
async def test_films_search_from_cache(make_get_request, prepare_es_index, populate_index, es_client):

    await prepare_es_index('testdata/movies.json')
    await populate_index('testdata/movies_data.json')

    response = await make_get_request('http://{0}:8000/api/v1/films/search/?query=Star&page_num=1&page_size=1'.format(config.api_ip))
    assert response.status == 200
    assert response.body[0]['uuid'] == '05d7341e-e367-4e2e-acf5-4652a8435f93'

    await es_client.options(ignore_status=[404]).indices.delete(index='movies')
    assert not await es_client.indices.exists(index='movies')

    response = await make_get_request('http://{0}:8000/api/v1/films/search/?query=Star&page_num=1&page_size=1'.format(config.api_ip))
    assert response.status == 200
    assert response.body[0]['uuid'] == '05d7341e-e367-4e2e-acf5-4652a8435f93'

