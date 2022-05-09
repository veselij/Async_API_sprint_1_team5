import json
from http import HTTPStatus

genre_pagination_wrong_params = [
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


genre_pagination_test_data = [
    (1, 1, 1, HTTPStatus.OK),
    (1, 2, 2, HTTPStatus.OK),
    (1, 10, 3, HTTPStatus.OK),
]

with open("testdata/genres_data.json", "r") as f:
    data = json.load(f)

genre_info_by_uuid_test = [
    ("3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", data[0]),
    ("120a21cf-9097-479e-904a-13dd7198c1dd", data[1]),
    ("b92ef010-5e4c-4fd0-99d6-41b6456272cd", data[2]),
]
