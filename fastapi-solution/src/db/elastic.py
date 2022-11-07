from typing import Optional

from db.search_engine import AsyncSearchEngine

es: Optional[AsyncSearchEngine] = None


async def get_elastic_storage() -> AsyncSearchEngine:
    """Возвращает экземпляр es."""
    return es
