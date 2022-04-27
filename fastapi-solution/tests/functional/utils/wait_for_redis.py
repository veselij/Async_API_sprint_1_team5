import asyncio
import os
import sys

import aioredis

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from settings import TestSettings


async def check_redis_ready():
    config = TestSettings()
    redis = await aioredis.create_redis("redis://{0}:{1}".format(config.redis_host, config.redis_port))
    while not await redis.ping():
        asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(check_redis_ready())
