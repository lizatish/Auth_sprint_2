import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

from tests.functional.settings import get_settings
from tests.functional.testdata.login import test_data_for_success_login_user, test_data_for_not_exists_login_user, \
    test_data_for_not_correct_password_login_user

conf = get_settings()
pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'request_body, expected_answer', test_data_for_success_login_user
)
def test_success_login_user(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        sync_redis_pool: Redis,
        request_body: dict,
        expected_answer: dict,
):
    from models.db_models import User

    response = auth_api_client.post('/login', json=request_body)
    response_body = response.json
    user = User.query.filter_by(username=request_body['username']).first()
    account_history = user.stories

    assert account_history
    assert user.username == request_body['username']
    assert response.status_code == expected_answer['status']
    assert response_body['access_token']
    assert response_body['refresh_token']
    assert sync_redis_pool.get(f"refresh_{user.id}").decode('ascii') == response_body['refresh_token']


@pytest.mark.parametrize(
    'request_body, expected_answer, expected_body', test_data_for_not_exists_login_user
)
def test_not_exists_login_user(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        sync_redis_pool: Redis,
        request_body: dict,
        expected_answer: dict,
        expected_body: str
):
    from models.db_models import User

    response = auth_api_client.post('/login', json=request_body)
    response_body = response.json
    user = User.query.filter_by(username=request_body['username']).first()

    assert not user
    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'request_body, expected_answer, expected_body', test_data_for_not_correct_password_login_user
)
def test_not_correct_password_login_user(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        sync_redis_pool: Redis,
        request_body: dict,
        expected_answer: dict,
        expected_body: str,
):
    response = auth_api_client.post('/login', json=request_body)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body
