import os
from datetime import timedelta
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Базовый класс конфигурации."""

    RATELIMIT_STRATEGY: str = "fixed-window"
    RATELIMIT_DEFAULT: str = "200 per day, 60 per hour"
    RATELIMIT_STORAGE_URI: str = "redis://"

    FACEBOOK_CLIENT_ID: str
    FACEBOOK_CLIENT_SECRET: str
    FACEBOOK_ACCESS_TOKEN_URL: str = 'https://graph.facebook.com/oauth/access_token'
    FACEBOOK_AUTHORIZE_URL: str = 'https://www.facebook.com/dialog/oauth'
    FACEBOOK_API_BASE_URL: str = 'https://graph.facebook.com/'
    FACEBOOK_CLIENT_KWARGS: dict = {'scope': 'email'}

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_SERVER_METADATA_URL: str = 'https://accounts.google.com/.well-known/openid-configuration'
    GOOGLE_CLIENT_KWARGS: dict = {'scope': 'openid email profile'}

    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_API_BASE_URL: str = 'https://login.yandex.ru/'
    YANDEX_AUTHORIZE_URL: str = 'https://oauth.yandex.com/authorize'
    YANDEX_ACCESS_TOKEN_URL: str = 'https://oauth.yandex.com/token'

    TWITTER_CLIENT_ID: str
    TWITTER_CLIENT_SECRET: str
    TWITTER_AUTHORIZE_URL: str = 'https://api.twitter.com/oauth/authenticate'
    TWITTER_REQUEST_TOKEN_URL: str = 'https://api.twitter.com/oauth/request_token'
    TWITTER_ACCESS_TOKEN_URL: str = 'https://api.twitter.com/oauth/access_token'

    PAGE: int = 1
    PER_PAGE: int = 5

    AUTH_PORT: int = 5555

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

    REDIS_LIMIT_URI: str = "redis://auth_redis:6379"
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

    REDIS_LIMIT_URI: str = "redis://localhost:6379"
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
