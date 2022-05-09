import json
from http import HTTPStatus


with open("testdata/movies_data.json", "r") as f:
    data = json.load(f)


test_data_num_outputs = [
    (1, 1, "Star", 1, HTTPStatus.OK),
    (1, 2, "Star", 2, HTTPStatus.OK),
    (2, 1, "Star", 1, HTTPStatus.OK),
    (2, 2, "Star", 1, HTTPStatus.NOT_FOUND),
]


film_pagination_test_data = [
    (1, 1, 1, HTTPStatus.OK),
    (1, 2, 2, HTTPStatus.OK),
    (1, 50, 3, HTTPStatus.OK),
]


film_pagination_wrong_params = [
    (
        "?page_num=-1&page_size=1",
        {
            "detail": [
                {
                    "loc": ["query", "page_num"],
                    "msg": "ensure this value is greater than or equal to 1",
                    "type": "value_error.number.not_ge",
                    "ctx": {"limit_value": 1},
                }
            ]
        },
    ),
    (
        "?page_num=1&page_size=-1",
        {
            "detail": [
                {
                    "loc": ["query", "page_size"],
                    "msg": "ensure this value is greater than or equal to 1",
                    "type": "value_error.number.not_ge",
                    "ctx": {"limit_value": 1},
                }
            ]
        },
    ),
]



film_full_info_by_uuid_test = [
    ("2a090dde-f688-46fe-a9f4-b781a985275e", HTTPStatus.OK, data[0]),
    ("05d7341e-e367-4e2e-acf5-4652a8435f93", HTTPStatus.OK, data[1]),
    ("15d7341e-e367-4e2e-acf5-4652a8435f93", HTTPStatus.OK, data[2]),
]

test_data_wrong_params = [
    (
        "",
        {
            "detail": [
                {
                    "loc": ["query", "query"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        },
    ),
    (
        "?query=Star&page_num=-1",
        {
            "detail": [
                {
                    "loc": ["query", "page_num"],
                    "msg": "ensure this value is greater than or equal to 1",
                    "type": "value_error.number.not_ge",
                    "ctx": {"limit_value": 1},
                }
            ]
        },
    ),
    (
        "?query=Star&page_size=-1",
        {
            "detail": [
                {
                    "loc": ["query", "page_size"],
                    "msg": "ensure this value is greater than or equal to 1",
                    "type": "value_error.number.not_ge",
                    "ctx": {"limit_value": 1},
                }
            ]
        },
    ),
]


test_non_exising_search = [
    ("", {"detail": "Films not found"}),
    ("Test", {"detail": "Films not found"}),
]


test_film_search_cache = [
    (
        "Star", {k:v for k,v in data[1].items() if k in ('uuid', 'title', 'imdb_rating')}
    ),
]


test_wrong_sort_data = [
("", {"detail":[{"loc":["query","sort"],"msg":"string does not match regex \"^-imdb_rating$|^imdb_rating$\"","type":"value_error.str.regex","ctx":{"pattern":"^-imdb_rating$|^imdb_rating$"}}]}),
("Test", {"detail":[{"loc":["query","sort"],"msg":"string does not match regex \"^-imdb_rating$|^imdb_rating$\"","type":"value_error.str.regex","ctx":{"pattern":"^-imdb_rating$|^imdb_rating$"}}]}),
]
