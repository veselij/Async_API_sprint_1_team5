from aioredis import Redis, ConnectionClosedError
from typing import Type

redis_client: Redis


async def get_redis() -> tuple[Redis, Type[Exception]]:
    return redis_client, ConnectionClosedError
