from typing import Optional

from elasticsearch import NotFoundError

from core.config import get_settings
from db.elastic import AsyncSearchEngine

conf = get_settings()


class SearchEngineService:
    """Сервис поиска."""

    def __init__(self, storage: AsyncSearchEngine, es_index: str):
        """Инициализация сервиса писка."""
        self.db = storage
        self.es_index = es_index

    async def search(self,
                     from_: int = None,
                     size: int = conf.ELASTIC_DEFAULT_OUTPUT_RECORDS_SIZE,
                     query: dict = None,
                     sort: str = None,
                     ) -> Optional[dict]:
        """Найти список документов в индексе."""
        try:
            doc = await self.db.search(
                index=self.es_index,
                from_=from_,
                size=size,
                query=query,
                sort=sort,
            )
        except NotFoundError:
            return None
        return doc['hits']['hits']

    async def get(self, doc_id: str) -> Optional[dict]:
        """Найти документ по идентификатору в индексе."""
        try:
            doc = await self.db.get(index=self.es_index, id=doc_id)
        except NotFoundError:
            return None
        return doc
