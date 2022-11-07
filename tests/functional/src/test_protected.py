import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

from tests.functional.settings import get_settings
from tests.functional.testdata.protected import test_data_protected_access, \
    test_data_protected_admin_access_only_failed, \
    test_data_protected_admin_access_only_successed

conf = get_settings()
pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'request_body, expected_answer, expected_body', test_data_protected_access
)
def test_protected_access(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        sync_redis_pool: Redis,
        request_body: dict,
        expected_answer: dict,
        expected_body: dict
):
    access_token = generate_access_token_for_user[request_body['username']]
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.get('/protected', headers=headers)
    response_body = response.json
    print(response_body)

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'user_data,  expected_answer, expected_body', test_data_protected_admin_access_only_failed
)
def test_protected_admin_access_only_get_user_data_failed(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        sync_redis_pool: Redis,
        user_data: dict,
        expected_answer: dict,
        expected_body: dict
):
    access_token = generate_access_token_for_user[user_data['username']]
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.get('/role-manager/2ef53946-d281-4a8f-92c4-09a63321daf2?label=privileged',
                                   headers=headers)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'user_data,  expected_answer, expected_body', test_data_protected_admin_access_only_successed
)
def test_protected_admin_access_only_get_user_data_successed(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        sync_redis_pool: Redis,
        user_data: dict,
        expected_answer: dict,
        expected_body: dict
):
    access_token = generate_access_token_for_user[user_data['username']]
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.get(
        '/role-manager/2ef53946-d281-4-09a63321daf2?label=privileged',
        headers=headers,
    )
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'user_data,  expected_answer, expected_body', test_data_protected_admin_access_only_failed
)
def test_protected_admin_access_only_delete_user_data_failed(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        sync_redis_pool: Redis,
        user_data: dict,
        expected_answer: dict,
        expected_body: dict
):
    access_token = generate_access_token_for_user[user_data['username']]
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.delete(f'/role-manager/2ef51-4a8f-92c4-09a63321daf2', headers=headers)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'user_data,  expected_answer, expected_body', test_data_protected_admin_access_only_successed
)
def test_protected_admin_access_only_delete_user_data_successed(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        sync_redis_pool: Redis,
        user_data: dict,
        expected_answer: dict,
        expected_body: dict
):
    access_token = generate_access_token_for_user[user_data['username']]
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.delete(f'/role-manager/2ef09a63321daf2', headers=headers)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body
