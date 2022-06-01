from typing import Type

from aioredis import ConnectionClosedError, Redis

redis_client: Redis


async def get_redis() -> tuple[Redis, Type[Exception]]:
    return redis_client, ConnectionClosedError
