import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from tests.functional.testdata.roles import (test_data_for_create_role_successful,
                                             test_data_for_create_role_fail,
                                             test_data_for_get_scope_roles,
                                             test_data_for_get_single_role,
                                             test_data_for_get_single_role_fail,
                                             test_data_for_delete_role,
                                             test_data_for_delete_role_fail,
                                             test_data_for_role_appoint_successful,
                                             test_data_for_role_appoint_fail,
                                             test_data_for_role_take_away_successful,
                                             test_data_for_role_take_away_fail)

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'request_body, expected_body, expected_answer', test_data_for_create_role_successful
)
async def test_create_role_successful(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        request_body: dict, expected_body: dict, expected_answer: dict
):
    """
    Тест для проверки успешных запросов на создание роли.

    Проверяет:
    - наличие роли после создания в бд
    - успешный ответ от сервиса
    """
    from models.db_models import Role
    access_token = generate_access_token_for_user['admin']
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.post('/role', json=request_body, headers=headers)
    response_body = response.json
    role = Role.query.filter_by(label=request_body['label']).first()

    assert role.label.value == request_body['label']
    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'request_body, expected_body, expected_answer', test_data_for_create_role_fail
)
async def test_create_role_fail(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        request_body: dict, expected_body: dict, expected_answer: dict
):
    """
    Тест для проверки неудачных запросов на создание роли.

    Проверяет:
    - отрицательный ответ от серивиса
    """
    access_token = generate_access_token_for_user['admin']
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.post('/role', json=request_body, headers=headers)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'expected_names, expected_answer', test_data_for_get_scope_roles
)
async def test_get_scope_roles(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        expected_names: list, expected_answer: dict
):
    """
    Тест для проверки получения списка ролей.

    Проверяет:
    - успещный ответ от серивиса
    - соответствие данных
    """
    access_token = generate_access_token_for_user['admin']
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.get('/role', headers=headers)
    response_body = response.json
    roles_names = [item['label'] for item in response_body]

    assert roles_names == expected_names
    assert response.status_code == expected_answer['status']
    assert len(response_body) == expected_answer['len']


@pytest.mark.parametrize(
    'role_id, expected_body, expected_answer', test_data_for_get_single_role
)
async def test_get_single_role(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        expected_body: list, expected_answer: dict, role_id: str
):
    """
    Тест для проверки получения одной роли.

    Проверяет:
    - ответ от серивиса
    - соответствие данных
    """
    access_token = generate_access_token_for_user['admin']
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.get(f'/role/{role_id}', headers=headers)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'role_id, expected_body, expected_answer', test_data_for_get_single_role_fail
)
async def test_get_single_role_fail(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        expected_body: list, expected_answer: dict, role_id: str
):
    """
    Тест для проверки получения одной роли.

    Проверяет:
    - ответ от серивиса
    - соответствие данных
    """
    access_token = generate_access_token_for_user['admin']
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.get(f'/role/{role_id}', headers=headers)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'role_id, expected_body, expected_answer', test_data_for_delete_role_fail
)
async def test_delete_role_fail(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        expected_body: list, expected_answer: dict, role_id: str
):
    """
    Тест для проверки неудачного удаления роли.

    Проверяет:
    - ответ от серивиса
    - соответствие данных
    """
    access_token = generate_access_token_for_user['admin']
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.delete(f'/role/{role_id}', headers=headers)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'role_id, expected_body, expected_answer', test_data_for_delete_role
)
async def test_delete_role(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        expected_body: list, expected_answer: dict, role_id: str
):
    """
    Тест для проверки неудачного удаления роли.

    Проверяет:
    - ответ от серивиса
    - соответствие данных
    """
    access_token = generate_access_token_for_user['admin']
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.delete(f'/role/{role_id}', headers=headers)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'user_id, role, expected_body, expected_answer', test_data_for_role_appoint_successful
)
async def test_role_appoint_successful(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        expected_body: list, expected_answer: dict, user_id: str, role: str
):
    """
    Тест для проверки успешной смены роли пользователя.

    Проверяет:
    - ответ от серивиса
    - соответствие данных
    """
    from models.db_models import User
    user_before = User.query.get(user_id)
    role_before = user_before.role
    access_token = generate_access_token_for_user['admin']
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.get(f'/role-manager/{user_id}?label={role}', headers=headers)
    response_body = response.json
    user_after = User.query.get(user_id)
    role_after = user_after.role

    assert role_before != role_after
    assert role_after.label == role
    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'user_id, role, expected_body, expected_answer', test_data_for_role_appoint_fail
)
async def test_role_appoint_fail(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        expected_body: list, expected_answer: dict, user_id: str, role: str
):
    """
    Тест для проверки неудачной смены роли пользователя.

    Проверяет:
    - ответ от серивиса
    - соответствие данных
    """
    access_token = generate_access_token_for_user['admin']
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.get(f'/role-manager/{user_id}?label={role}', headers=headers)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'user_id, expected_body, expected_answer', test_data_for_role_take_away_successful
)
async def test_role_take_away_successful(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        expected_body: list, expected_answer: dict, user_id: str
):
    """
    Тест для проверки неудачной смены роли пользователя.

    Проверяет:
    - ответ от серивиса
    - соответствие данных
    """

    access_token = generate_access_token_for_user['admin']
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.delete(f'/role-manager/{user_id}', headers=headers)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'user_id, expected_body, expected_answer', test_data_for_role_take_away_fail
)
async def test_role_take_away_fail(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        expected_body: list, expected_answer: dict, user_id: str
):
    """
    Тест для проверки неудачной смены роли пользователя.

    Проверяет:
    - ответ от серивиса
    - соответствие данных
    """
    access_token = generate_access_token_for_user['admin']
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.delete(f'/role-manager/{user_id}', headers=headers)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body
