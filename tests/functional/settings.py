import logging
from datetime import timedelta
from functools import lru_cache

from pydantic import BaseSettings


class TestSettings(BaseSettings):
    """Базовые тестовые настройки."""

    PAGE: int = 1
    PER_PAGE: int = 5

    AUTH_PORT: int = 4555

    # Настройки Flask
    TESTING: bool = True
    SECRET_KEY: str = 'secret-key'
    FLASK_ENV: str = 'test_production'

    DEFAULT_ROLE_NAME: str = 'standard'

    # Настройки логирования
    LOG_LEVEL: int = logging.DEBUG

    # Настройки Redis
    CACHE_REVOKED_ACCESS_TOKEN_EXPIRED_SEC: int = timedelta(hours=1).total_seconds()
    CACHE_REFRESH_TOKEN_EXPIRED_SEC: int = timedelta(days=30).total_seconds()
    CACHE_PORT: int = 6379
    CACHE_HOST: str

    # Настройки Postgres
    POSTGRES_DB_NAME: str
    POSTGRES_DB_USER: str
    POSTGRES_DB_PASSWORD: str
    POSTGRES_DB_HOST: str
    POSTGRES_DB_PORT: int = 5432

    AUTH_HASH_METHOD: str
    AUTH_HASH_SALT_LENGTH: int


class TestSettingsDocker(TestSettings):
    """Тестовые настройки для развертки приложения через docker."""

    # Настройки Redis
    CACHE_HOST: str = 'test_auth_redis'

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI: str

    # Настройки Postgres
    POSTGRES_DB_HOST: str = 'test_auth_postgres'

    class Config:
        """Дополнительные базовые настройки."""

        env_file = '.env.local'
        env_file_encoding = 'utf-8'


class TestSettingsLocal(TestSettings):
    """Тестовые настройки для развертки приложения локально."""

    # Настройки Redis
    CACHE_HOST: str = 'localhost'

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI: str

    # Настройки Postgres
    POSTGRES_DB_HOST: str = 'localhost'

    class Config:
        """Дополнительные базовые настройки."""

        env_file = '../.env.local.local'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> TestSettings:
    """Возвращает настройки тестов."""
    return TestSettingsLocal()
