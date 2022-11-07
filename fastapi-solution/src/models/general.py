from typing import Optional, Literal

from pydantic import BaseModel, Field

from models.common import UUIDMixin


class PersonFilm(BaseModel):
    """Модель представления вложенного фильма внутри персоны."""

    role: Literal['actor', 'writer', 'director']
    film_ids: set[str]


class Person(UUIDMixin):
    """Модель персонажа."""

    full_name: str = Field(..., alias='name')
    films: list[Optional[PersonFilm]] = []


class Genre(UUIDMixin):
    """Модель жанра."""

    name: str
    description: Optional[str]


class Film(UUIDMixin):
    """Модель кинопроизведения."""

    title: str
    imdb_rating: float
    description: Optional[str]
    genres: list[Genre] = []
    actors: list[Person] = []
    writers: list[Person] = []
    directors: list[Person] = []
    age_limit: int = 0
