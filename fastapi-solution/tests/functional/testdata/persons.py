import json

with open("testdata/persons_data.json", "r") as f:
    data = json.load(f)

person_info_by_uuid_test = [
    ("01377f6d-9767-48ce-9e37-3c81f8a3c739", data[0]),
    ("035c4793-4864-45b8-8d4f-b86b454c60b0", data[1]),
    ("09ea7635-dfee-4722-ad40-23c93ef03644", data[2]),
]

person_info_search_test = [
    ("Woody", data[0]),
]

person_films = [
    (
        "01377f6d-9767-48ce-9e37-3c81f8a3c739",
        [
            {
                "uuid": "2a090dde-f688-46fe-a9f4-b781a985275e",
                "title": "Star Wars: Knights of the Old Republic",
                "imdb_rating": 9.6,
            }
        ],
    ),
]
