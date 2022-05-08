import pytest

from settings import config
from testdata.persons import person_info_by_uuid_test



@pytest.mark.asyncio
@pytest.mark.parametrize('uuid,result', person_info_by_uuid_test)
async def test_person_by_uuid(
    uuid,
    result,
    make_get_request,
    prepare_es_index,
    populate_index,
    clear_redis,
    ):

    await prepare_es_index("testdata/persons.json")
    await populate_index("testdata/persons_data.json")

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/persons/{uuid}'
    )

    assert response.status == 200
    assert response.body == result


@pytest.mark.asyncio
async def test_person_films(
    make_get_request,
    prepare_es_index,
    populate_index,
    clear_redis,
    ):
    
    await prepare_es_index("testdata/movies.json")
    await populate_index("testdata/movies_data.json")
    await prepare_es_index("testdata/persons.json")
    await populate_index("testdata/persons_data.json")

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/persons/01377f6d-9767-48ce-9e37-3c81f8a3c739/films'
    )

    assert response.status == 200
    assert response.body == [{
        "uuid": "2a090dde-f688-46fe-a9f4-b781a985275e",
        "title": "Star Wars: Knights of the Old Republic",
        "imdb_rating": 9.6,
    }]


@pytest.mark.asyncio
async def test_person_search(
    make_get_request,
    prepare_es_index,
    populate_index,
    clear_redis,
    ):
    
    await prepare_es_index("testdata/movies.json")
    await populate_index("testdata/movies_data.json")
    await prepare_es_index("testdata/persons.json")
    await populate_index("testdata/persons_data.json")

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/persons/search/?query=Woody'
    )

    assert response.status == 200
    assert response.body == [{
        "uuid":"01377f6d-9767-48ce-9e37-3c81f8a3c739",
        "full_name":"Woody Harrelson",
        "role":"actor",
        "film_ids":["57beb3fd-b1c9-4f8a-9c06-2da13f95251c,2a090dde-f688-46fe-a9f4-b781a985275e"]
    }]



@pytest.mark.asyncio
async def test_person_cashe(
    make_get_request,
    prepare_es_index,
    populate_index,
    es_client,
    clear_redis,
    ):

    await prepare_es_index("testdata/persons.json")
    await populate_index("testdata/persons_data.json")

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/persons/01377f6d-9767-48ce-9e37-3c81f8a3c739'
    )

    assert response.status == 200
    assert response.body == {
        "uuid":"01377f6d-9767-48ce-9e37-3c81f8a3c739",
        "full_name":"Woody Harrelson",
        "role":"actor",
        "film_ids":["57beb3fd-b1c9-4f8a-9c06-2da13f95251c,2a090dde-f688-46fe-a9f4-b781a985275e"]
    }


    await es_client.options(ignore_status=[404]).indices.delete(index="movies")
    assert not await es_client.indices.exists(index="movies")

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/persons/01377f6d-9767-48ce-9e37-3c81f8a3c739'
    )

    assert response.status == 200
    assert response.body == {
        "uuid":"01377f6d-9767-48ce-9e37-3c81f8a3c739",
        "full_name":"Woody Harrelson",
        "role":"actor",
        "film_ids":["57beb3fd-b1c9-4f8a-9c06-2da13f95251c,2a090dde-f688-46fe-a9f4-b781a985275e"]
    }
