from typing import Optional, Any


def get_query_film_by_genre(genre: Optional[str]) -> dict[str, Any]:
    if genre is not None:
        return {
            "query": {
                "nested": {
                    "path": "genre",
                    "query": {
                        "term": {
                                "genre.uuid": genre
                        }
                    }
                }
            }
        }
    return {"query": None}


def get_query_film_search(search_word: str) -> dict[str, Any]:
    return {
        "query": {
            "multi_match": {
                "query": search_word,
                "fuzziness": "auto",
                "fields": [
                    "title",
                    "description"
                ]
            }
        }
    }
