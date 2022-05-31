from typing import Any, Optional


def get_query_film_by_genre(genre: Optional[str]) -> dict[str, Any]:
    if genre is not None:
        return {"query": {"nested": {"path": "genre", "query": {"term": {"genre.uuid": genre}}}}}
    return {"query": None}


def prepare_subscriptions_filter(subsriptions: list) -> list:
    filter = []
    for subscrption in subsriptions:
        element = {"nested": {"path": "actors", "query": {"term": {"actors.name": subscrption}}}}
        filter.append(element)
    return element


def get_query_film_search(search_word: str, subscriptions: list) -> dict[str, Any]:
    return {
        "query": {
            "bool": {
                "must": [{
                    "multi_match": {"query": search_word, "fuzziness": "auto", "fields": ["title", "description"]}
                },{"filter": [{"bool": {"should": prepare_subscriptions_filter(subscriptions)}}]}]
            }
        }
    }


def _get_query_film_search(search_word: str) -> dict[str, Any]:
    return {"query": {"multi_match": {"query": search_word, "fuzziness": "auto", "fields": ["title", "description"]}}}


def get_query_person_search(search_word: str) -> dict[str, Any]:
    return {"query": {"multi_match": {"query": search_word, "fuzziness": "auto", "fields": ["full_name"]}}}


def get_query_films_by_person(person: str) -> dict[str, Any]:
    return {
        "query": {
            "bool": {
                "should": [
                    {"nested": {"path": "actors", "query": {"term": {"actors.uuid": person}}}},
                    {"nested": {"path": "writers", "query": {"term": {"writers.uuid": person}}}},
                    {"nested": {"path": "directors", "query": {"term": {"directors.uuid": person}}}},
                ]
            }
        }
    }
