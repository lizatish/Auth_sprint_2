import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncIterator

import aioredis
import pytest
import pytest_asyncio
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

from core.app_factory import create_app
from db import redis
from db.db_factory import get_db
from tests.functional.settings import get_settings
from tests.functional.testdata.postgresdata import users_data, redis_users_expires_data
from tests.functional.testdata.generate_tokens import users_data_for_tokens
from tests.functional.testdata.postgresdata import roles_data
from tests.functional.testdata.postgresdata import users_data, redis_users_expires_data, users_data_for_tokens


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    """Фикстура главного цикла событий."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def redis_pool(app: Flask) -> AsyncIterator[Redis]:
    """Фикстура соединения с redis."""
    pool = aioredis.from_url(
        f"redis://{app.config['CACHE_HOST']}:{app.config['CACHE_PORT']}", encoding="utf-8", decode_responses=True
    )
    yield pool
    await pool.close()


@pytest_asyncio.fixture(scope="session")
def app() -> Flask:
    """Фикстура главного приложения."""
    settings = get_settings()
    app = create_app(settings)
    yield app


@pytest.fixture(scope="session")
def sync_redis_pool(app) -> Redis:
    """Временная фикстура синхронного redis."""
    redis = Redis(
        host=app.config['CACHE_HOST'],
        port=app.config['CACHE_PORT'],
    )

    for user, user_expires_delta in zip(users_data, redis_users_expires_data):
        token_user_data = {"username": user["username"], "role": user["role"]}
        with app.app_context():
            refresh_token = create_refresh_token(identity=token_user_data, expires_delta=user_expires_delta)
        redis.set(
            f"refresh_{user['id']}",
            refresh_token,
            app.config['CACHE_REFRESH_TOKEN_EXPIRED_SEC'],
        )

    yield redis
    redis.flushall()


@pytest.fixture()
def auth_api_client(app: Flask, sync_redis_pool: Redis) -> FlaskClient:
    """Фикстура апи-клиента."""
    redis.cache = sync_redis_pool
    yield app.test_client()


@pytest.fixture(scope="session")
def generate_access_token_for_user(app):
    result = {}
    with app.app_context():
        for item in users_data_for_tokens:
            result[item['username']] = create_access_token(identity=item)
    yield result


@pytest.fixture(scope="session")
def sqlalchemy_postgres(app: Flask) -> SQLAlchemy:
    """Фикстура алхимии для бд postgres c заполненными данными о персонах."""
    from models.db_models import User, Role
    with app.app_context():
        db = get_db()

        for role_data in roles_data:
            role = Role(**role_data)
            db.session.add(role)
            db.session.commit()

        for user_data in users_data:
            role = Role.query.filter_by(label=user_data['role']).first()
            user = User(
                id=user_data['id'],
                username=user_data['username'],
                password=user_data['password'],
                role=role
            )
            db.session.add(user)
            db.session.commit()
        yield db

        users = User.query.all()
        for user in users:
            db.session.delete(user)
            db.session.commit()

        roles = Role.query.all()
        for role in roles:
            db.session.delete(role)
            db.session.commit()


@pytest.fixture(scope="session")
def generate_access_token_for_user(app) -> dict:
    """Сгенерированные валидные access_token-ы для всех пользователей"""
    result = {}
    with app.app_context():
        for item in users_data_for_tokens:
            result[item['username']] = create_access_token(identity=item)
    yield result
