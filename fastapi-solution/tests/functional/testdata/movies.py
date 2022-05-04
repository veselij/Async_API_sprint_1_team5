test_data_num_outputs = [
(1, 1, 'Star', 1, 200),
(1, 2, 'Star', 2, 200),
(2, 1, 'Star', 1, 200),
(2, 2, 'Star', 1, 404),
]

test_data_wrong_params = [
("", {"detail":[{"loc":["query","query"],"msg":"field required","type":"value_error.missing"}]}),
("?query=Star&page_num=-1", {"detail":[{"loc":["query","page_num"],"msg":"ensure this value is greater than or equal to 1","type":"value_error.number.not_ge","ctx":{"limit_value":1}}]}),
("?query=Star&page_size=-1", {"detail":[{"loc":["query","page_size"],"msg":"ensure this value is greater than or equal to 1","type":"value_error.number.not_ge","ctx":{"limit_value":1}}]}),
]
