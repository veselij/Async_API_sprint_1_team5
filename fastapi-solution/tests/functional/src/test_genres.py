import pytest
from http import HTTPStatus

from settings import config
from testdata.genres import genre_pagination_wrong_params, genre_pagination_test_data, genre_info_by_uuid_test


@pytest.mark.asyncio
@pytest.mark.parametrize('params,results', genre_pagination_wrong_params)
async def test_genre_pagination_wrong_params(params, results, make_get_request, clear_redis):

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/genres/{params}'
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
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

    response = await  make_get_request(
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

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/genres/{uuid}'
    )

    assert response.status == HTTPStatus.OK
    assert response.body == result


@pytest.mark.asyncio
@pytest.mark.parametrize('uuid,result', genre_info_by_uuid_test)
async def test_genre_cashe(
    uuid,
    result,
    make_get_request,
    prepare_es_index,
    populate_index,
    es_client,
    clear_redis,
    ):

    await prepare_es_index("testdata/genres.json")
    await populate_index("testdata/genres_data.json")

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/genres/{uuid}'
    )

    assert response.status == HTTPStatus.OK
    assert response.body == result


    await es_client.options(ignore_status=[404]).indices.delete(index="movies")
    assert not await es_client.indices.exists(index="movies")

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/genres/{uuid}'
    )

    assert response.status == HTTPStatus.OK
    assert response.body == result


