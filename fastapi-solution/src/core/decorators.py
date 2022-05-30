import asyncio
import hashlib
import json
import logging
from functools import wraps

from core.exceptions import RetryExceptionError
from db import redis


def cache(expire: int = 60):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            redis_client, _ = await redis.get_redis()
            cache_key = hashlib.md5(
                "{0}_{1}_{2}_{3}".format(
                    func.__module__,
                    func.__name__,
                    args,
                    kwargs,
                ).encode(),
            ).hexdigest()
            cache_value = await redis_client.get(cache_key)
            if cache_value is not None:
                return json.loads(cache_value)
            value = await func(*args, **kwargs)
            if isinstance(value, list):
                await redis_client.set(
                    cache_key,
                    json.dumps([model.dict() for model in value]),
                    expire=expire,
                )
            else:
                await redis_client.set(cache_key, value.json(), expire=expire)
            return value

        return inner

    return wrapper


def expo(start_sleep_time, factor, border_sleep_time):
    """Generate exponential sequence.

    Args:
        start_sleep_time: float start repeat time
        factor: int exponential factor
        border_sleep_time: int exponential limit

    Description:
        t = start_sleep_time * factor^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time

    Yields:
        float: exponential sequence member
    """
    start = start_sleep_time
    sequence_element = 1
    while True:
        yield start
        start = start_sleep_time * factor**sequence_element
        if start > border_sleep_time:
            start = border_sleep_time
        sequence_element += 1


def backoff_async(logger: logging.Logger, start_sleep_time: float = 0.1, factor: int = 2, border_sleep_time: int = 10):
    """Repeat function with exponential delay in case it raises RetryException.

    Args:
        start_sleep_time: float start repeat time
        factor: int exponential factor
        border_sleep_time: int exponential limit
    """
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            delays = expo(start_sleep_time, factor, border_sleep_time)
            func_result = None
            while True:
                try:
                    func_result = await func(*args, **kwargs)
                except RetryExceptionError as e:
                    logger.exception(e)
                    delay = next(delays)
                else:
                    break
                asyncio.sleep(delay)
            return func_result
        return inner
    return func_wrapper
