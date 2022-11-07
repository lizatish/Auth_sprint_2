from functools import lru_cache
from typing import Optional

from fastapi import Depends

from core.config import get_settings
from db.elastic import get_elastic_storage
from db.redis import get_redis_storage
from db.cache import AsyncCacheStorage
from db.search_engine import AsyncSearchEngine
from models.common import FilterSimpleValues, FilterNestedValues
from services.cache import CacheService
from services.search_engine import SearchEngineService
from models.general import Film, Person, PersonFilm

conf = get_settings()


class FilmService:
    """Сервис для работы с фильмами."""

    def __init__(self, cache_storage: AsyncCacheStorage, search_engine_storage: AsyncSearchEngine):
        """Инициализация сервиса."""
        self.cache_service = CacheService(cache_storage)
        self.search_engine_service = SearchEngineService(search_engine_storage, 'movies')
        self.person_roles = ['writers', 'actors', 'directors']

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        """Функция для получения фильма по id."""
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)
        return film

    async def get_scope_films(
            self, paginate_from: int, paginate_size: int, search_filter: dict, sort: str, url: str,
    ) -> Optional[list[Film]]:
        """Функция для получения списка фильмов."""
        films = await self._films_from_cache(url)
        if not films:
            films = await self._get_scope_films_from_elastic(
                paginate_from=paginate_from, paginate_size=paginate_size, sort=sort, search_filter=search_filter,
            )
            if films:
                await self._put_films_to_cache(films, url)
        return films

    async def search_film(
            self, search_query: str, paginate_from: int, search_size: int, url: str,
    ) -> Optional[list[Film]]:
        """Функция для поиска фильма."""
        films = await self._films_from_cache(url)
        if not films:
            films = await self._search_film_from_elastic(
                search_query=search_query, paginate_from=paginate_from, paginate_size=search_size,
            )
            if films:
                await self._put_films_to_cache(films, url)
        return films

    async def get_films_by_person(self, person_id: str) -> list[Optional[Film]]:
        """Возвращает фильмы, в которых участвовала персона."""
        films = await self._films_from_cache(f'film_by_person_{person_id}')
        if not films:
            docs = await self._get_by_person_ids_from_elastic([person_id])
            if docs:
                films = [Film(**doc['_source']) for doc in docs]
                await self._put_films_to_cache(films, f'film_by_person_{person_id}')

        return films

    async def get_person_by_id(self, person_id: str) -> Optional[Person]:
        """Возвращает персону по идентификатору."""
        person = await self._person_from_cache(f'info_{person_id}')
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)
        return person

    async def get_person_by_ids(self, person_ids: list[str]) -> list[Person]:
        """Возвращает набор персон по списку идентификаторов."""
        persons = await self._persons_from_cache('-'.join(person_ids))
        if not persons:
            persons = []
            docs = await self._get_by_person_ids_from_elastic(person_ids)
            for person_id in person_ids:
                person = await self._prepare_person(person_id, docs)
                persons.append(person)
            await self._put_persons_to_cache(persons, '-'.join(person_ids))
        return persons

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        """Возвращает персону из эластика."""
        docs = await self._get_by_person_ids_from_elastic([person_id])
        return await self._prepare_person(person_id, docs)

    async def _search_film_from_elastic(
            self, search_query: str, paginate_from: int, paginate_size: int,
    ) -> Optional[list[Film]]:
        """Функция для поиска фильма в elasticsearch."""
        query = {
            'multi_match': {
                'query': f'{search_query}',
                'fuzziness': 'auto',
            },
        }
        docs = await self.search_engine_service.search(from_=paginate_from, size=paginate_size, query=query)
        if not docs:
            return docs
        return [Film(**hit['_source']) for hit in docs]

    async def _get_scope_films_from_elastic(
            self, paginate_from: int, paginate_size: int, search_filter: dict, sort: str,
    ) -> Optional[list[Film]]:
        """Функция для поиска фильмов в elasticsearch в соот. фильтрам."""
        if search_filter:
            filter_nested_values = FilterNestedValues.get_values()
            filter_simple_values = FilterSimpleValues.get_values()
            query = []
            for key in search_filter:
                if key in filter_nested_values:
                    query.append(
                        {
                            'nested': {
                                'path': f'{key}',
                                'query': {
                                    'bool': {
                                        'must': [
                                            {
                                                'match': {
                                                    f'{key}.id': f'{search_filter[key]}',
                                                },
                                            },
                                        ],
                                    },
                                },
                            },
                        },
                    )
                elif key in filter_simple_values:
                    query.append({'match': {f'{key}': f'{search_filter[key]}'}})

            doc = await self.search_engine_service.search(
                from_=paginate_from,
                size=paginate_size,
                sort=f'{sort[1:]}:desc' if sort[0] == '-'
                else f'{sort}:asc',
                query={'bool': {'must': query}},
            )
        else:
            doc = await self.search_engine_service.search(
                from_=paginate_from,
                size=paginate_size,
                sort=f'{sort[1:]}:desc' if sort[0] == '-'
                else f'{sort}:asc',
            )
        return [Film(**hit['_source']) for hit in doc]

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        """Функция для поиска фильма в elasticsearch по id."""
        doc = await self.search_engine_service.get(doc_id=film_id)
        if not doc:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        """Функция отдаёт фильм по id если он есть в кэше."""
        data = await self.cache_service.get(film_id)
        if not data:
            return None
        return Film.parse_raw(data)

    async def _put_film_to_cache(self, film: Film):
        """Функция кладёт фильм по id в кэш."""
        await self.cache_service.set(
            film.id, film.json(), expire=conf.FILM_CACHE_EXPIRE_IN_SECONDS,
        )

    async def _person_from_cache(self, person_id: str) -> Optional[Person]:
        """Возвращает персону ид кеша редиса."""
        data = await self.cache_service.get(person_id)
        if not data:
            return None
        person = Person.parse_raw(data)
        return person

    async def _prepare_person(self, person_id: str, docs: dict) -> Person:
        """Подготавливает полные данные по персоне и возвращает их."""
        person = None
        persons_roles = {}
        for doc in docs:
            source = doc['_source']

            for role in self.person_roles:
                dirty_person_roles = list(filter(lambda x: x['id'] == person_id, source[role]))
                person_roles = list({v['id']: v for v in dirty_person_roles}.values())
                if not person_roles:
                    continue

                person_id, person_name = person_roles[0]['id'], person_roles[0]['name']
                if role not in persons_roles:
                    persons_roles[role] = {
                        'id': person_id,
                        'full_name': person_name,
                        'fw_ids': [source['id']],
                    }
                else:
                    persons_roles[role]['fw_ids'].append(source['id'])

        for role, role_data in persons_roles.items():
            person_film = PersonFilm(role=role[:-1], film_ids=set(role_data['fw_ids']))
            if not person:
                person = Person(
                    id=role_data['id'],
                    full_name=role_data['full_name'],
                    films=[person_film])
            else:
                for ix, exists_person_film in enumerate(person.films):
                    if exists_person_film.role == role[:-1]:
                        person.films[ix].film_ids |= set(role_data['fw_ids'])
                        break
                else:
                    person.films.append(person_film)

        return person

    async def _get_by_person_ids_from_elastic(self, person_ids: list[str]) -> dict:
        """Возвращает результат запроса к elastic для поиска персон."""
        return await self.search_engine_service.search(
            query={
                'bool': {
                    'should': [
                        {
                            'nested': {
                                'path': 'writers',
                                'query': {
                                    'terms': {
                                        'writers.id': person_ids,
                                    },
                                },
                            },
                        },
                        {
                            'nested': {
                                'path': 'actors',
                                'query': {
                                    'terms': {
                                        'actors.id': person_ids,
                                    },
                                },
                            },
                        },
                        {
                            'nested': {
                                'path': 'directors',
                                'query': {
                                    'terms': {
                                        'directors.id': person_ids,
                                    },
                                },
                            },
                        },
                    ],
                },
            },
        )

    async def _films_from_cache(self, url: str):
        """Функция отдаёт список фильмов если они есть в кэше."""
        data = await self.cache_service.lrange(url, 0, -1)
        if not data:
            return None
        films = [Film.parse_raw(item) for item in data]
        return reversed(films)

    async def _put_films_to_cache(self, films: list[Film], url: str):
        """Функция кладёт список фильмов в кэш."""
        data = [item.json() for item in films]
        await self.cache_service.lpush(
            url, *data,
        )
        await self.cache_service.expire(url, conf.FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _persons_from_cache(self, url: str):
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

    async def _put_person_to_cache(self, person: Person):
        """Получает персону из кеша редиса."""
        await self.cache_service.set(f'info_{person.id}', person.json(), expire=conf.PERSON_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        cache_storage: AsyncCacheStorage = Depends(get_redis_storage),
        search_engine_storage: AsyncSearchEngine = Depends(get_elastic_storage),
) -> FilmService:
    """Возвращает экземпляр сервиса для работы с кинопроизведениями."""
    return FilmService(cache_storage, search_engine_storage)
