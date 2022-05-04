import asyncio

import aioredis

from settings import config


async def check_redis_ready():
    redis = await aioredis.create_redis("redis://{0}:{1}".format(config.redis_host, config.redis_port))
    while not await redis.ping():
        asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(check_redis_ready())
