import hashlib
import json
from db import redis
from functools import wraps


def cache(expire: int = 60):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            redis_client = await redis.get_redis()
            cache_key = hashlib.md5("{0}_{1}_{2}_{3}".format(func.__module__, func.__name__, args, kwargs).encode()).hexdigest()
            cache_value = await redis_client.get(cache_key)
            if cache_value is not None:
                return json.loads(cache_value)
            value = await func(*args, **kwargs)
            if isinstance(value, list):
                await redis_client.set(cache_key, json.dumps([model.dict() for model in value]), expire=expire)
            else:
                await redis_client.set(cache_key, value.json(), expire=expire)
            return value
        return inner
    return wrapper
