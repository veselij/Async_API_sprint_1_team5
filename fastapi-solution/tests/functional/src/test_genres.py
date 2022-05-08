import pytest

from settings import config
from testdata.genres import genre_pagination_wrong_params, genre_pagination_test_data, genre_info_by_uuid_test


@pytest.mark.asyncio
@pytest.mark.parametrize('params,results', genre_pagination_wrong_params)
async def test_genre_pagination_wrong_params(params, results, make_get_request, clear_redis):

    response = make_get_request(
        f'http://{config.api_ip}:8000/api/v1/genres/{params}'
    )

    assert response.status == 422
    assert response.body == results


@pytest.mark.asyncio
@pytest.mark.parametrize('page_num,page_size,results_len,status_code', genre_pagination_test_data)
async def test_genres(
    page_num,
    page_size,
    results_len,
    status_code,
    prepare_es_index,
    populate_index,
    make_get_request,
    clear_redis,
    ):

    await prepare_es_index("testdata/genres.json")
    await populate_index("testdata/genres_data.json")

    response = make_get_request(
        f'http://{config.api_ip}:8000/api/v1/genres/?page_num={page_num}&page_size={page_size}'
    )

    assert response.status == status_code
    assert len(response.body) == results_len

@pytest.mark.asyncio
@pytest.mark.parametrize('uuid,result', genre_info_by_uuid_test)
async def test_genre_by_uuid(
    uuid,
    result,
    make_get_request,
    prepare_es_index,
    populate_index,
    clear_redis,
    ):

    await prepare_es_index("testdata/genres.json")
    await populate_index("testdata/genres_data.json")

    response = make_get_request(
        f'http://{config.api_ip}:8000/api/v1/genres/{uuid}'
    )

    assert response.status == 200
    assert len(response.body) == result

@pytest.mark.asyncio
async def test_genre_cashe(
    make_get_request,
    prepare_es_index,
    populate_index,
    es_client,
    clear_redis,
    ):

    await prepare_es_index("testdata/genres.json")
    await populate_index("testdata/genres_data.json")

    response = make_get_request(
        f'http://{config.api_ip}:8000/api/v1/genres/3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff'
    )

    assert response.status == 200
    assert response.body == [{
        "uuid": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
        "name": "Action",
        "description": ""
    }]


    await es_client.options(ignore_status=[404]).indices.delete(index="movies")
    assert not await es_client.indices.exists(index="movies")

    response = make_get_request(
        f'http://{config.api_ip}:8000/api/v1/genres/3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff'
    )

    assert response.status == 200
    assert response.body == [{
        "uuid": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
        "name": "Action",
        "description": ""
    }]


