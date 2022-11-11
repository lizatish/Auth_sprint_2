from flask import Flask
from flask_limiter import Limiter
import redis
from flask_limiter.util import get_remote_address

limiter: Limiter | None = None


def create_limiter(app: Flask):
    """Инициализирует limiter."""
    global limiter
    with app.app_context():
        pool = redis.connection.BlockingConnectionPool.from_url(app.config['REDIS_LIMIT_URI'])
        limiter = Limiter(
            app, key_func=get_remote_address,
            storage_options={"connection_pool": pool},
        )


def get_limiter_instance() -> Limiter:
    """Возвращает экземпляр limiter."""
    return limiter
