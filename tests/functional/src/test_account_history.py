import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from tests.functional.testdata.account_history import test_data_for_get_account_history


pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize(
    'request_body, expected_answer', test_data_for_get_account_history
)
async def test_get_account_history(
        auth_api_client: FlaskClient, sqlalchemy_postgres: SQLAlchemy,
        request_body: dict, expected_answer: dict
):
    """
    Тест для проверки получения списка входов пользователя.
    Проверяет:
    - успещный ответ от серивиса
    - соответствие данных
    """
    response_1 = auth_api_client.post('/login', json=request_body)
    response_body_1 = response_1.json

    headers = {'Authorization': f'Bearer {response_body_1["access_token"]}'}
    response = auth_api_client.get('/account-history', headers=headers)
    response_body = response.json

    assert response_body['results'][0]['created']
    assert response_body['results'][0]['id']
    assert len(response_body['results']) == expected_answer['len']
    assert response.status_code == expected_answer['status']
