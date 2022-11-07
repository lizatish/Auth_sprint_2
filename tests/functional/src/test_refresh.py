from datetime import timedelta

import pytest
from flask.testing import FlaskClient
from flask_jwt_extended import create_refresh_token, get_jwt
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

from tests.functional.settings import get_settings
from tests.functional.testdata.refresh import test_data_for_update_user_refresh_token, \
    test_data_unsuccess_usage_old_refresh_token, test_data_unsuccess_update_user_refresh_token_not_exists, \
    test_data_unsuccess_update_user_refresh_token_another_role, \
    test_data_unsuccess_update_user_refresh_token_validation_error
from tests.functional.utils.tokens import get_revoked_access_tokens

conf = get_settings()
pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'user_data, expected_answer', test_data_for_update_user_refresh_token
)
def test_success_update_user_refresh_token(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        sync_redis_pool: Redis,
        user_data: dict,
        expected_answer: dict,
):
    from models.db_models import User
    user = User.query.filter_by(username=user_data['username']).first()
    old_refresh_token = sync_redis_pool.get(f"refresh_{user.id}").decode('ascii')
    headers = {'Authorization': f'Bearer {old_refresh_token}', 'content-type': 'application/json'}

    response = auth_api_client.post('/refresh', headers=headers)
    response_body = response.json
    refresh_token = sync_redis_pool.get(f"refresh_{user.id}").decode('ascii')

    revoked_tokens = get_revoked_access_tokens(user.id, sync_redis_pool)
    access_token_jwt = get_jwt()["jti"]

    assert len(revoked_tokens) == 1
    assert revoked_tokens[0].decode('ascii') == access_token_jwt

    assert response.status_code == expected_answer['status']
    assert response_body['access_token']
    assert response_body['refresh_token']
    assert response_body['refresh_token'] != old_refresh_token
    assert refresh_token == response_body['refresh_token']


@pytest.mark.parametrize(
    'user_data, expected_answer, expected_body', test_data_unsuccess_usage_old_refresh_token
)
def test_unsuccess_usage_old_refresh_token(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        sync_redis_pool: Redis,
        user_data: dict,
        expected_answer: dict,
        expected_body: dict
):
    from models.db_models import User
    user = User.query.filter_by(username=user_data['username']).first()
    old_refresh_token = sync_redis_pool.get(f"refresh_{user.id}").decode('ascii')
    headers = {'Authorization': f'Bearer {old_refresh_token}', 'content-type': 'application/json'}

    good_response = auth_api_client.post('/refresh', headers=headers)
    bad_response = auth_api_client.post('/refresh', headers=headers)

    assert bad_response.json == expected_body
    assert bad_response.status_code == expected_answer['status']
    assert sync_redis_pool.get(f"refresh_{user.id}").decode('ascii') == good_response.json['refresh_token']


@pytest.mark.parametrize(
    'user_data, expected_answer, expected_body', test_data_unsuccess_update_user_refresh_token_not_exists
)
def test_unsuccess_update_user_refresh_token_not_exists(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        sync_redis_pool: Redis,
        user_data: dict,
        expected_answer: dict,
        expected_body: dict
):
    refresh_token = create_refresh_token(identity=user_data, expires_delta=timedelta(days=30))
    headers = {'Authorization': f'Bearer {refresh_token}', 'content-type': 'application/json'}

    response = auth_api_client.post('/refresh', headers=headers)
    assert response.json == expected_body
    assert response.status_code == expected_answer['status']


@pytest.mark.parametrize(
    'user_data, expected_answer, expected_body', test_data_unsuccess_update_user_refresh_token_another_role
)
def test_unsuccess_update_user_refresh_token_another_role(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        sync_redis_pool: Redis,
        user_data: dict,
        expected_answer: dict,
        expected_body: dict
):
    from models.db_models import User
    refresh_token = create_refresh_token(identity=user_data, expires_delta=timedelta(days=30))
    headers = {'Authorization': f'Bearer {refresh_token}', 'content-type': 'application/json'}

    response = auth_api_client.post('/refresh', headers=headers)
    user = User.query.filter_by(username=user_data['username']).first()

    assert response.json == expected_body
    assert user
    assert response.status_code == expected_answer['status']


@pytest.mark.parametrize(
    'refresh_token, expected_answer, expected_body', test_data_unsuccess_update_user_refresh_token_validation_error
)
def test_unsuccess_update_user_refresh_token_validation_error(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        sync_redis_pool: Redis,
        refresh_token: dict,
        expected_answer: dict,
        expected_body: dict
):
    headers = {'Authorization': f'Bearer {refresh_token}', 'content-type': 'application/json'}
    response = auth_api_client.post('/refresh', headers=headers)

    assert response.json == expected_body
    assert response.status_code == expected_answer['status']
