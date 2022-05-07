import json

test_data_num_outputs = [
(1, 1, 'Star', 1, 200),
(1, 2, 'Star', 2, 200),
(2, 1, 'Star', 1, 200),
(2, 2, 'Star', 1, 404),
]

film_pagination_test_data = [
    (1, 1, 1, 200),
    (1, 2, 2, 200),
    (1, 50, 50, 200),
]

film_pagination_wrong_params = {
    ("?page_num=-1&page_size=1", {"detail":[{"loc":["query","page_num"],"msg":"ensure this value is greater than or equal to 1","type":"value_error.number.not_ge","ctx":{"limit_value":1}}]}),
    ("?page_num=1&page_size=-1", {"detail":[{"loc":["query","page_size"],"msg":"ensure this value is greater than or equal to 1","type":"value_error.number.not_ge","ctx":{"limit_value":1}}]}),
}

with open('testdata/movies_data.json', 'r') as f:
            data = json.load(f)

film_full_info_by_uuid_test = [
    ('2a090dde-f688-46fe-a9f4-b781a985275e', data[0]),
    ('05d7341e-e367-4e2e-acf5-4652a8435f93', data[1]),
    ('15d7341e-e367-4e2e-acf5-4652a8435f93', data[3]),
]

test_data_wrong_params = [
("", {"detail":[{"loc":["query","query"],"msg":"field required","type":"value_error.missing"}]}),
("?query=Star&page_num=-1", {"detail":[{"loc":["query","page_num"],"msg":"ensure this value is greater than or equal to 1","type":"value_error.number.not_ge","ctx":{"limit_value":1}}]}),
("?query=Star&page_size=-1", {"detail":[{"loc":["query","page_size"],"msg":"ensure this value is greater than or equal to 1","type":"value_error.number.not_ge","ctx":{"limit_value":1}}]}),
]
