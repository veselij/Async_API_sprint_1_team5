import pytest

from settings import config
from testdata.movies import film_pagination_wrong_params, film_pagination_test_data, film_full_info_by_uuid_test



@pytest.mark.asyncio
@pytest.mark.parametrize('sort', ['', 'Test'])
async def test_films_main_page_wrong_sort(sort, make_get_request, clear_redis):

    response = await make_get_request(f'http://{config.api_ip}:8000/api/v1/films/?sort={sort}')

    assert response.status == 422
    assert response.body == {"detail":[{"loc":["query","sort"],"msg":"string does not match regex \"^-imdb_rating$|^imdb_rating$\"","type":"value_error.str.regex","ctx":{"pattern":"^-imdb_rating$|^imdb_rating$"}}]}


@pytest.mark.asyncio
@pytest.mark.parametrize('params,results', film_pagination_wrong_params)
async def test_films_pagination_wrong_params(params, results, make_get_request, clear_redis):

    response = await make_get_request(f'http://{config.api_ip}:8000/api/v1/films/{params}')

    assert response.status == 422
    assert response.body == results


@pytest.mark.asyncio
@pytest.mark.parametrize('page_num,page_size,results_len,code', film_pagination_test_data)
async def test_films_pagination(page_num, page_size, results_len, code, make_get_request, clear_redis, prepare_es_index, populate_index):

    await prepare_es_index("testdata/movies.json")
    await populate_index("testdata/movies_data.json")

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/films/?page_num={page_num}&page_size={page_size}'
        )

    assert response.status == code
    assert len(response.body) == results_len


@pytest.mark.asyncio
@pytest.mark.parametrize('uuid, code, expected_response', film_full_info_by_uuid_test)
async def test_film_full_info(
    uuid,
    code,
    expected_response,
    make_get_request,
    prepare_es_index,
    populate_index,
    clear_redis,
):

    await prepare_es_index("testdata/movies.json")
    await populate_index("testdata/movies_data.json")

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/films/{uuid}'
    )

    assert response.status == code
    assert response.body == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize('uuid, code, expected_response', film_full_info_by_uuid_test)
async def test_film_full_info_cashe(
    uuid,
    code,
    expected_response,
    make_get_request,
    prepare_es_index,
    populate_index,
    es_client,
    clear_redis,
):

    await prepare_es_index("testdata/movies.json")
    await populate_index("testdata/movies_data.json")

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/films/{uuid}'
    )

    assert response.status == code
    assert response.body == expected_response

    await es_client.options(ignore_status=[404]).indices.delete(index="movies")
    assert not await es_client.indices.exists(index="movies")

    response = await make_get_request(
        f'http://{config.api_ip}:8000/api/v1/films/{uuid}'
    )

    assert response.status == code
    assert response.body == expected_response
