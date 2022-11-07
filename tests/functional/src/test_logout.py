import time
from datetime import timedelta

import pytest
from flask.testing import FlaskClient
from flask_jwt_extended import get_jwt, create_access_token
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

from tests.functional.settings import get_settings
from tests.functional.testdata.logout import test_data_for_test_success_logout, \
    test_data_for_test_failed_logout_token_revoked, test_data_for_test_failed_logout_token_expired
from tests.functional.utils.tokens import get_revoked_access_tokens

conf = get_settings()
pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'user_data, expected_answer, expected_body', test_data_for_test_success_logout
)
def test_success_logout(
        auth_api_client: FlaskClient,
        generate_access_token_for_user: dict,
        sqlalchemy_postgres: SQLAlchemy,
        sync_redis_pool: Redis,
        user_data: dict,
        expected_answer: dict,
        expected_body: str
):
    from models.db_models import User
    user = User.query.filter_by(username=user_data['username']).first()
    access_token = generate_access_token_for_user[user_data['username']]
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.post('/logout', headers=headers)
    response_body = response.json
    revoked_tokens = get_revoked_access_tokens(user.id, sync_redis_pool)
    access_token_jwt = get_jwt()["jti"]
    refresh_token = sync_redis_pool.get(f"refresh_{user.id}")

    assert not refresh_token
    assert len(revoked_tokens) == 1
    assert revoked_tokens[0].decode('ascii') == access_token_jwt
    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'user_data, expected_answer, expected_body', test_data_for_test_failed_logout_token_revoked
)
def test_failed_logout_token_revoked(
        auth_api_client: FlaskClient,
        generate_access_token_for_user: dict,
        sqlalchemy_postgres: SQLAlchemy,
        sync_redis_pool: Redis,
        user_data: dict,
        expected_answer: dict,
        expected_body: str
):
    access_token = generate_access_token_for_user[user_data['username']]
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    auth_api_client.post('/logout', headers=headers)
    response = auth_api_client.post('/logout', headers=headers)
    assert response.status_code == expected_answer['status']
    assert response.json == expected_body


@pytest.mark.parametrize(
    'user_data, expected_answer, expected_body', test_data_for_test_failed_logout_token_expired
)
def test_failed_logout_token_expired(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        sync_redis_pool: Redis,
        user_data: dict,
        expected_answer: dict,
        expected_body: str
):
    sleep_time = 0.0001
    access_token = create_access_token(identity=user_data, expires_delta=timedelta(seconds=sleep_time))
    time.sleep(sleep_time)
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.post('/logout', headers=headers)

    assert response.status_code == expected_answer['status']
    assert response.json == expected_body
