import pytest
from http import HTTPStatus

from settings import config
from testdata.persons import person_info_by_uuid_test, person_info_search_test, person_films



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

    assert response.status == HTTPStatus.OK
    assert response.body == result


@pytest.mark.asyncio
@pytest.mark.parametrize('uuid,result', person_films)
async def test_person_films(
    uuid,
    result,
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
        f'http://{config.api_ip}:8000/api/v1/persons/{uuid}/films'
    )

    assert response.status == HTTPStatus.OK
    assert response.body == result


@pytest.mark.asyncio
@pytest.mark.parametrize('query,result', person_info_search_test)
async def test_person_search(
    query,
    result,
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
        f'http://{config.api_ip}:8000/api/v1/persons/search/?query={query}'
    )

    assert response.status == HTTPStatus.OK
    assert response.body == [result]



@pytest.mark.asyncio
@pytest.mark.parametrize('uuid,result', person_info_by_uuid_test)
async def test_person_cashe(
    uuid,
    result,
    make_get_request,
    prepare_es_index,
    populate_index,
    es_client,
    clear_redis,
    ):

    await prepare_es_index("testdata/persons.json")
    await populate_index("testdata/persons_data.json")

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/persons/{uuid}'
    )

    assert response.status == HTTPStatus.OK
    assert response.body == result


    await es_client.options(ignore_status=[404]).indices.delete(index="movies")
    assert not await es_client.indices.exists(index="movies")

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/persons/{uuid}'
    )

    assert response.status == HTTPStatus.OK
    assert response.body == result
