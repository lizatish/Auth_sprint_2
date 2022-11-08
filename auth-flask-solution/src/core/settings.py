import os
from datetime import timedelta
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Базовый класс конфигурации."""

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_CLIENT_CONF_URL: str

    PAGE: int = 1
    PER_PAGE: int = 5

    AUTH_PORT: int = 5000

    # Базовые настройки приложения
    SECRET_KEY: str

    # Настройки аутентификации
    AUTH_HASH_METHOD: str
    AUTH_HASH_SALT_LENGTH: int

    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = 'auth'

    # Стандартное название роли
    DEFAULT_ROLE_NAME: str = 'standard'

    # Настройки Redis
    CACHE_REVOKED_ACCESS_TOKEN_EXPIRED_SEC: int = timedelta(hours=1).total_seconds()
    CACHE_REFRESH_TOKEN_EXPIRED_SEC: int = timedelta(days=30).total_seconds()
    CACHE_HOST: str
    CACHE_PORT: int = 6379

    # Корень проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProdSettings(Settings):
    """Настройки для развертки приложения."""

    FLASK_ENV: str = 'production'
    DEBUG: bool = False
    TESTING: bool = False

    # Настройки Redis
    CACHE_HOST: str = 'auth_redis'

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://auth_postgres'

    class Config:
        """Дополнительные базовые настройки."""

        env_file = '.env'
        env_file_encoding = 'utf-8'


class DevSettings(Settings):
    """Настройки для разработки приложения;"""

    FLASK_ENV: str = 'development'
    DEBUG: bool = True
    TESTING: bool = True

    # Настройки Redis
    CACHE_HOST: str = 'localhost'

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI: str

    class Config:
        """Дополнительные базовые настройки."""

        env_file = '../../.env.local'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    """Возвращает настройки тестов."""
    return DevSettings()
