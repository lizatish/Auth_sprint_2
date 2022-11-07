from typing import Optional, Literal

from pydantic import BaseModel


class PersonFilm(BaseModel):
    """Вложенная модель для описания фильмов по персоне."""

    role: Literal['actor', 'writer', 'director']
    film_ids: set[str]


class Person(BaseModel):
    """Модель фильма для ответа пользователю."""

    uuid: str
    full_name: str
    films: list[Optional[PersonFilm]] = []


class FilmByPerson(BaseModel):
    """Модель для представления получения фильмов по персоне."""

    uuid: str
    title: str
    imdb_rating: float
