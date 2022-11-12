import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = 'movies'

    # Настройки Redis
    CACHE_HOST: str = '127.0.0.1'
    CACHE_PORT: int = 6379

    # Настройки Elasticsearch
    ELASTIC_HOST: str = '127.0.0.1'
    ELASTIC_PORT: int = 9200
    ELASTIC_DEFAULT_OUTPUT_RECORDS_SIZE: int = 10000

    # Корень проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Время хранения данных в кэше
    FILM_CACHE_EXPIRE_IN_SECONDS: int = 60 * 5
    GENRE_CACHE_EXPIRE_IN_SECONDS: int = 60 * 5
    PERSON_CACHE_EXPIRE_IN_SECONDS: int = 60 * 5

    AUTH_SERVICE_PROTECTED = 'http://127.0.0.1:4555/auth/v1/users/protected'
    DEFAULT_USER_ROLE = 'ANONYMOUS'

    class Config:
        """Дополнительные базовые настройки."""

        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    """Возвращает настройки тестов."""
    return Settings()
