import asyncio
import logging

import aioredis
from settings import config

from utils.backoff import backoff
from utils.exceptions import RetryExceptionError

logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh = logging.FileHandler(filename="/var/log/waiters/redis.log")
fh.setFormatter(formatter)
logger.addHandler(fh)


@backoff(logger, start_sleep_time=0.1, factor=2, border_sleep_time=10)
async def check_redis_ready():
    redis = await aioredis.create_redis("redis://{0}:{1}".format(config.redis_host, config.redis_port))
    if not await redis.ping():
        raise RetryExceptionError("Redis is not ready")


if __name__ == '__main__':
    asyncio.run(check_redis_ready())
