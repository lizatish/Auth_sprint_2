from db.cache import CacheStorage

cache: CacheStorage | None = None


def get_redis_storage() -> CacheStorage:
    """Возвращает экземпляр redis."""
    return cache
