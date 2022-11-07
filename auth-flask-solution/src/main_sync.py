from redis import Redis

from core.app_factory import create_app
from core.settings import get_settings
from db import redis

settings = get_settings()
app = create_app(settings)

redis.cache = Redis(
    host=app.config['CACHE_HOST'],
    port=app.config['CACHE_PORT'],
)

if __name__ == '__main__':
    app.run(port=app.config['AUTH_PORT'])
