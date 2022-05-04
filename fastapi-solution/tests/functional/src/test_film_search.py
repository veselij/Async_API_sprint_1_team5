import pytest

from settings import config
from testdata.movies import test_data_num_outputs, test_data_wrong_params



@pytest.mark.asyncio
@pytest.mark.parametrize("query", ["", "Test"])
async def test_films_search_not_existing(query, make_get_request, clear_redis):

    response = await make_get_request("http://{0}:8000/api/v1/films/search/?query={1}".format(config.api_ip, query))

    assert response.status == 404
    assert response.body == {"detail": "Films not found"}


@pytest.mark.asyncio
@pytest.mark.parametrize("params,results", test_data_wrong_params)
async def test_films_search_missing_required_parameter(params, results, make_get_request, clear_redis):

    response = await make_get_request("http://{0}:8000/api/v1/films/search/{1}".format(config.api_ip, params))

    assert response.status == 422
    assert response.body == results


@pytest.mark.asyncio
@pytest.mark.parametrize("page_num,page_size,query,number,code", test_data_num_outputs)
async def test_films_search(
    page_num,
    page_size,
    query,
    number,
    code,
    make_get_request,
    prepare_es_index,
    populate_index,
    clear_redis,
):

    await prepare_es_index("testdata/movies.json")
    await populate_index("testdata/movies_data.json")

    response = await make_get_request(
        "http://{0}:8000/api/v1/films/search/?query={1}&page_num={2}&page_size={3}".format(
            config.api_ip, query, page_num, page_size
        )
    )

    assert response.status == code
    assert len(response.body) == number


@pytest.mark.asyncio
async def test_films_search_from_cache(make_get_request, prepare_es_index, populate_index, es_client, clear_redis):

    await prepare_es_index("testdata/movies.json")
    await populate_index("testdata/movies_data.json")

    response = await make_get_request(
        "http://{0}:8000/api/v1/films/search/?query=Star&page_num=1&page_size=1".format(config.api_ip)
    )
    assert response.status == 200
    assert response.body == [
        {
            "uuid": "05d7341e-e367-4e2e-acf5-4652a8435f93",
            "title": "The Secret World of Jeffree Star",
            "imdb_rating": 9.5,
        }
    ]

    await es_client.options(ignore_status=[404]).indices.delete(index="movies")
    assert not await es_client.indices.exists(index="movies")

    response = await make_get_request(
        "http://{0}:8000/api/v1/films/search/?query=Star&page_num=1&page_size=1".format(config.api_ip)
    )
    assert response.status == 200
    assert response.body == [
        {
            "uuid": "05d7341e-e367-4e2e-acf5-4652a8435f93",
            "title": "The Secret World of Jeffree Star",
            "imdb_rating": 9.5,
        }
    ]
