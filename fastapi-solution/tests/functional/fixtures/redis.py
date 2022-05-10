import pytest

import aioredis

from settings import config

@pytest.fixture(scope="session")
async def redis_client():
    client = await aioredis.create_redis_pool("redis://{0}:{1}".format(config.redis_host, config.redis_port))
    yield client
    client.close()
    await client.wait_closed()


@pytest.fixture
async def clear_redis(redis_client):
    await redis_client.flushall(async_op=False)
