from typing import Optional

from pydantic import BaseModel


class Genre(BaseModel):
    """Схема жанра."""

    uuid: str
    name: str


class Person(BaseModel):
    """Схема персоны."""

    uuid: str
    full_name: str


class Film(BaseModel):
    """Схема фильма."""

    uuid: str
    title: str
    imdb_rating: float
    description: Optional[str]
    genres: list[Genre] = []
    actors: list[Person] = []
    writers: list[Person] = []
    directors: list[Person] = []


class ShortFilm(BaseModel):
    """Схема урезанной версии фильма."""

    uuid: str
    title: str
    imdb_rating: float
