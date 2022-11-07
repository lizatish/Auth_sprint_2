import asyncio

import aioredis

from tests.functional.logger import get_logger
from tests.functional.settings import get_settings
from tests.functional.utils.connection import async_backoff

conf = get_settings()
logger = get_logger()


@async_backoff(
    Exception,
    backoff_logger=logger,
)
async def connect_redis():
    """Ожидание подключения к redis"""
    redis_client = aioredis.from_url(
        f"redis://{conf.CACHE_HOST}:{conf.CACHE_PORT}", encoding="utf-8", decode_responses=True
    )
    logger.debug('Connection to redis established!')
    await redis_client.close()


if __name__ == '__main__':
    asyncio.run(connect_redis())
