import logging

import aioredis
import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.v1 import films, genres, persons
from core.config import get_settings
from core.logger import LOGGING
from core.middleware import MyMiddleware
from db import elastic
from db import redis

conf = get_settings()

app = FastAPI(
    title=conf.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)
my_middleware = MyMiddleware(some_attribute="some_attribute_here_if_needed")
app.add_middleware(BaseHTTPMiddleware, dispatch=my_middleware)

@app.on_event('startup')
async def startup():
    """Метод, выполняющий инициализацию компонентов приложения при старте."""
    redis.cache = aioredis.from_url(
        f"redis://{conf.CACHE_HOST}:{conf.CACHE_PORT}", encoding="utf-8", decode_responses=True
    )
    elastic.es = AsyncElasticsearch(hosts=[f'http://{conf.ELASTIC_HOST}:{conf.ELASTIC_PORT}'])


@app.on_event('shutdown')
async def shutdown():
    """Метод, выполняющий утилизацию компонентов приложения после завершения работы  приложения."""
    await redis.cache.close()
    await elastic.es.close()


app.include_router(films.router, tags=['films'])
app.include_router(genres.router, tags=['genres'])
app.include_router(persons.router, tags=['persons'])



if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
