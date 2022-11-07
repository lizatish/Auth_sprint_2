from functools import lru_cache
from typing import Optional

from fastapi import Depends

from core.config import get_settings
from services.search_engine import SearchEngineService
from services.cache import CacheService
from db.elastic import get_elastic_storage
from db.redis import get_redis_storage
from db.cache import AsyncCacheStorage
from db.search_engine import AsyncSearchEngine
from models.general import Genre

conf = get_settings()


class GenreService:
    """Сервис для работы с жанрами."""

    def __init__(self, cache_storage: AsyncCacheStorage, search_engine_storage: AsyncSearchEngine):
        """Инициализация сервиса."""
        self.cache_service = CacheService(cache_storage)
        self.search_engine_service = SearchEngineService(search_engine_storage, 'genres')

    async def get_genres_list(self, url: str) -> list[Genre]:
        """Возвращает список всех жанров."""
        genres = await self._genres_from_cache(url)
        if not genres:
            docs = await self.search_engine_service.search(query={'match_all': {}})
            genre_docs = docs
            if genre_docs:
                genres = [Genre(**genre_doc['_source']) for genre_doc in genre_docs]
                await self._put_genres_to_cache(genres, url)
        return genres

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        """Возвращает жанр по идентификатору."""
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if genre:
                await self._put_genre_to_cache(genre)
        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        """Получает жанр из elastic."""
        genre = None
        query = {
            'bool': {
                'must': [
                    {
                        'match_phrase': {
                            'id': genre_id,
                        },
                    },
                ],
            },
        }
        doc = await self.search_engine_service.search(query=query)
        if doc:
            genre = Genre(**doc[0]['_source'])

        return genre

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.cache_service.get(genre_id)
        if not data:
            return None

        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        await self.cache_service.set(genre.id, genre.json(), expire=conf.GENRE_CACHE_EXPIRE_IN_SECONDS)

    async def _genres_from_cache(self, url: str):
        """Функция отдаёт список жанров если они есть в кэше."""
        data = await self.cache_service.lrange(url, 0, -1)
        if not data:
            return None
        genres = [Genre.parse_raw(item) for item in data]
        return reversed(genres)

    async def _put_genres_to_cache(self, genres: list[Genre], url: str):
        """Функция кладёт список жанров в кэш."""
        data = [item.json() for item in genres]
        await self.cache_service.lpush(
            url, *data,
        )
        await self.cache_service.expire(url, conf.GENRE_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        cache_storage: AsyncCacheStorage = Depends(get_redis_storage),
        search_engine_storage: AsyncSearchEngine = Depends(get_elastic_storage),
) -> GenreService:
    """Возвращает экземпляр сервиса для работы с жанрами."""
    return GenreService(cache_storage, search_engine_storage)
