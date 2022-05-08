import json

genre_pagination_wrong_params = [
    ("?page_num=-1&page_size=1", {"detail":[{"loc":["query","page_num"],"msg":"ensure this value is greater than or equal to 1","type":"value_error.number.not_ge","ctx":{"limit_value":1}}]}),
    ("?page_num=1&page_size=-1", {"detail":[{"loc":["query","page_size"],"msg":"ensure this value is greater than or equal to 1","type":"value_error.number.not_ge","ctx":{"limit_value":1}}]}),
]


genre_test_data = [
    (1, 1, 1, 200),
    (1, 2, 2, 200),
    (1, 10, 10, 200),
]

with open('testdata/genres_data.json', 'r') as f:
            data = json.load(f)

genre_info_by_uuid_test = [
    ('2a090dde-f688-46fe-a9f4-b781a985275e', data[0]),
    ('05d7341e-e367-4e2e-acf5-4652a8435f93', data[1]),
    ('15d7341e-e367-4e2e-acf5-4652a8435f93', data[2]),
]

