from db.redis import AsyncCacheStorage


class CacheService:
    """Сервис кеширования."""

    def __init__(self, storage: AsyncCacheStorage):
        """Инициализация сервиса."""
        self.db = storage

    async def get(self, key: str) -> str:
        """Возвращает элементы по ключу."""
        return await self.db.get(key)

    async def set(self, key: str, value: str, expire: int) -> str:
        """Записывает ключ для хранения значения."""
        return await self.db.set(key, value, expire)

    async def lrange(self, key: str, start: int, stop: int) -> list:
        """Возвращает диапазон значений, лежащих по ключу."""
        return await self.db.lrange(key, start, stop)

    async def lpush(self, key: str, *elements: list[str]) -> int:
        """Кладет элемент в список по ключу в начало очереди."""
        return await self.db.lpush(key, *elements)

    async def expire(self, key: str, seconds: int) -> bool:
        """Задает время, после которого ключ станет невалидным."""
        return await self.db.expire(key, seconds)
