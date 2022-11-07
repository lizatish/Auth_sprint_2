import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from tests.functional.settings import get_settings
from tests.functional.testdata.users_change_data import (test_data_for_change_data_successfull,
                                                         test_data_for_change_data_fail)

conf = get_settings()
pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'user, request_body, expected_body, expected_answer', test_data_for_change_data_successfull
)
async def test_change_user_data_successfull(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy, generate_access_token_for_user,
        request_body: dict, expected_body: dict, expected_answer: dict, user: dict
):
    """
    Тест для проверки успешных запросов на изменение данных пользователя.

    Проверяет:
    - что данные в бд поменялся
    - успешный ответ от серивиса
    """
    from models.db_models import User

    token = generate_access_token_for_user[user['username']]
    headers = {'Authorization': f'Bearer {token}', 'content-type': 'application/json'}
    user_before_change = User.query.get(user['id'])
    username_before = user_before_change.username

    response = auth_api_client.put(f'/user', json=request_body, headers=headers)
    response_body = response.json
    user_after_change = User.query.get(user['id'])
    username_after = user_after_change.username

    assert username_before != username_after
    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'user, request_body, expected_body, expected_answer', test_data_for_change_data_fail
)
async def test_change_user_data_fail(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy, generate_access_token_for_user,
        request_body: dict, expected_body: dict, expected_answer: dict, user: dict
):
    """
    Тест для проверки ошибки смены данных пользователя.

    Проверяет:
    - неудачный ответ от серивиса
    """
    token = generate_access_token_for_user[user['username']]
    headers = {'Authorization': f'Bearer {token}', 'content-type': 'application/json'}

    response = auth_api_client.put(f'/user', json=request_body, headers=headers)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body
