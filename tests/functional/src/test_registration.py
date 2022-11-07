import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from tests.functional.settings import get_settings
from tests.functional.testdata.users_registration import (test_data_for_registration_successfull,
                              test_data_for_registration_fail)

conf = get_settings()
pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize(
    'request_body, expected_body, expected_answer', test_data_for_registration_successfull
)
async def test_registration_successfull(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy,
        request_body: dict, expected_body: dict, expected_answer: dict
):
    """
    Тест для проверки успешных запросов на регистрацию.

    Проверяет:
    - наличие пользователя после регистрации в бд
    - успешный ответ от серивиса
    """
    from models.db_models import User

    response = auth_api_client.post(f'/registration', json=request_body)
    response_body = response.json
    user = User.query.filter_by(username=request_body['username']).first()

    assert user.username == request_body['username']
    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'request_body, expected_body, expected_answer', test_data_for_registration_fail
)
async def test_registration_fail(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy,
        request_body: dict, expected_body: dict, expected_answer: dict
):
    """
    Тест для проверки ошибки регистрации при существовании пользователя с таким логином.

    Проверяет:
    - неудачный ответ от серивиса
    """
    auth_api_client.post(f'/registration', json=request_body)

    response = auth_api_client.post(f'/registration', json=request_body)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body
