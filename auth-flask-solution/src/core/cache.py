from flask import Flask
from flask_caching import Cache

cache: Cache | None = None


def create_cache(app: Flask):
    """Инициализирует cache."""
    global cache
    cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
    with app.app_context():
        cache.init_app(app)


def get_cache_instance() -> Cache:
    """Возвращает экземпляр cache."""
    return cache
