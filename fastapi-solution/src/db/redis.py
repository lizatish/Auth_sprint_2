from typing import Optional

from db.cache import AsyncCacheStorage

cache: Optional[AsyncCacheStorage] = None


async def get_redis_storage() -> AsyncCacheStorage:
    """Возвращает экземпляр redis."""
    return cache
