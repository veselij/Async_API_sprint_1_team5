from aioredis import Redis

redis_client: Redis


async def get_redis() -> Redis:
    return redis_client
