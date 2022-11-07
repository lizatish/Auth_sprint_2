from functools import lru_cache
from typing import Optional

from fastapi import Depends

from core.config import get_settings
from db.elastic import get_elastic_storage
from db.redis import get_redis_storage
from db.cache import AsyncCacheStorage
from db.search_engine import AsyncSearchEngine
from models.general import Person
from services.search_engine import SearchEngineService
from services.cache import CacheService

conf = get_settings()


class PersonService:
    """Сервис для работы с участниками фильма."""

    def __init__(self, cache_storage: AsyncCacheStorage, search_engine_storage: AsyncSearchEngine):
        """Инициализация сервиса."""
        self.cache_service = CacheService(cache_storage)
        self.search_engine_service = SearchEngineService(search_engine_storage, 'persons')

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        """Возвращает участника фильма по идентификатору."""
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person.id, person)
        return person

    async def search_person(self, query: str, from_: int, size: int, url: str) -> Optional[list[Person]]:
        """Возвращает совпадения по персоне."""
        persons = await self._persons_from_cache(url)
        if not persons:
            persons = await self._search_person_from_elastic(query=query, from_=from_, size=size)
            if not persons:
                return None
            await self._put_persons_to_cache(persons, url)
        return persons

    async def _search_person_from_elastic(self, query: str, from_: int, size: int) -> list[Person]:
        """Ищет данные по персоне в индексе персон."""
        if query:
            doc = await self.search_engine_service.search(
                from_=from_,
                size=size,
                query={
                    'multi_match': {
                        'query': f'{query}',
                        'fuzziness': 'auto',
                    },
                },
            )
        else:
            doc = await self.search_engine_service.search(
                from_=from_,
                size=size,
            )
        return [Person(**hit['_source']) for hit in doc]

    async def enrich_person_data(self, main_person_info: Person, fw_person_info: Person) -> Person:
        """Обогащает данные по персоне, возвращает полные данные по персоне."""
        enriched_id = f'enriched_{main_person_info.id}'
        person = await self._person_from_cache(enriched_id)
        if not person:
            person = main_person_info.copy()
            person.films = fw_person_info.films.copy()
            await self._put_person_to_cache(enriched_id, person)
        return person

    async def _enriched_person_from_cache(self, person_id: str) -> Optional[Person]:
        """Получает персону из кеша редиса."""
        data = await self.cache_service.get(f'enriched_{person_id}')
        if not data:
            return None
        person = Person.parse_raw(data)
        return person

    async def _put_enriched_person_to_cache(self, person: Person):
        """Кладет персону в кеш редиса."""
        await self.cache_service.set(f'enriched_{person.id}', person.json(), expire=conf.PERSON_CACHE_EXPIRE_IN_SECONDS)

    async def _person_from_cache(self, person_id: str) -> Optional[Person]:
        """Кладет персону в кеш редиса."""
        data = await self.cache_service.get(person_id)
        if not data:
            return None
        person = Person.parse_raw(data)
        return person

    async def _put_person_to_cache(self, person_id: str, person: Person):
        """Получает персону из кеша редиса."""
        await self.cache_service.set(person_id, person.json(), expire=conf.PERSON_CACHE_EXPIRE_IN_SECONDS)

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        """Возвращает персону из эластика."""
        person = None
        doc = await self.search_engine_service.search(
            query={
                'bool': {
                    'must': [
                        {
                            'match_phrase': {
                                'id': person_id,
                            },
                        },
                    ],
                },
            },
        )
        if doc:
            person = Person(**doc[0]['_source'])

        return person

    async def enrich_persons_list_data(self, persons: list[Person], fw_person_info: list[Person], url) -> list[Person]:
        """Возвращает полный список персон с расширенными данными."""
        enriched_url = f'enriched_{url}'
        full_persons = await self._persons_from_cache(enriched_url)
        if not full_persons:
            full_persons = []
            for person_base, person_fw in zip(persons, fw_person_info):
                if person_fw:
                    full_person = await self.enrich_person_data(person_base, person_fw)
                else:
                    full_person = person_base
                full_persons.append(full_person)
            await self._put_persons_to_cache(full_persons, enriched_url)
        return full_persons

    async def _persons_from_cache(self, url: str) -> Optional[list]:
        """Функция отдаёт список персон если они есть в кэше."""
        data = await self.cache_service.lrange(url, 0, -1)
        if not data:
            return None
        persons = [Person.parse_raw(item) for item in data]
        return list(reversed(persons))

    async def _put_persons_to_cache(self, persons: list[Person], url: str):
        """Функция кладёт список персон в кэш."""
        data = [item.json() for item in persons]
        await self.cache_service.lpush(url, *data)
        await self.cache_service.expire(url, conf.PERSON_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_person_service(
        cache_storage: AsyncCacheStorage = Depends(get_redis_storage),
        search_engine_storage: AsyncSearchEngine = Depends(get_elastic_storage),
) -> PersonService:
    """Возвращает экземпляр сервиса для работы с участниками фильма."""
    return PersonService(cache_storage, search_engine_storage)
