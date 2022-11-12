import re
from http import HTTPStatus

import requests
from fastapi import Query, Request, HTTPException
from pydantic import BaseModel

from core.config import get_settings
from models.common import FilterNestedValues, FilterSimpleValues

conf = get_settings()


class RoleRequired:
    """Класс для проверки ролей и доступов."""

    def __init__(self, *roles: str):
        """Инициализация требования ролей."""
        self.roles = roles

    async def __call__(self, request: Request):
        """Проверка токена доступа и роли пользователя"""
        token = request.headers.get('Authorization')

        try:
            response = requests.get(
                f'http://{conf.AUTH_SERVICE_HOST}:{conf.AUTH_SERVICE_PORT}/auth/v1/users/protected',
                headers={"Authorization": token}
            )
            response_body = response.json()
            if response.status_code == HTTPStatus.OK:
                role = response_body['msg']
            else:
                role = 'ANONYMOUS'
        except Exception:
            role = 'ANONYMOUS'

        if role not in self.roles:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='You don\'t have permissions for this action',
            )


class Paginator(BaseModel):
    """Модель для пагинации."""

    page_size: int = Query(default=50, alias='size', ge=1)
    page_number: int = Query(default=0, alias='number')


def validate_filter_values(filter_: dict) -> dict:
    """Валидирует фильтр запроса."""
    result_filter = {}

    filter_nested_values = FilterNestedValues.get_values()
    filter_simple_values = FilterSimpleValues.get_values()

    for key, val in filter_.items():
        if key in filter_nested_values or key in filter_simple_values:
            result_filter[key] = val

    return result_filter


def get_filter(req: Request) -> dict:
    """Функция преобразует данные для фильтрации из запроса  к необходимому виду."""
    filter_ = {}
    for key, value in req.query_params.items():
        if re.match('^filter\\[[a-zA-Z_]{0,25}\\]$', key) is not None:
            filter_[key.replace('filter[', '').replace(']', '')] = value

    return validate_filter_values(filter_)
