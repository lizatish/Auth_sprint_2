import datetime
import re
from uuid import UUID

from pydantic import BaseModel, validator
from flask import current_app

from models.general import RoleType


class UserLoginScheme(BaseModel):
    username: str
    password: str


class RefreshAccessTokensResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserRegistration(BaseModel):
    """Схема регистрации."""

    username: str
    password: str

    @validator("password")
    def check_storage_type(cls, value):
        pattern = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.fullmatch(pattern, value):
            raise ValueError('Минимум восемь символов, минимум одна буква и одна цифра.')
        return value


class PasswordChange(BaseModel):
    """Схема смены пароля."""

    old_password: str
    new_password: str

    @validator("new_password")
    def check_storage_type(cls, value):
        pattern = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.fullmatch(pattern, value):
            raise ValueError('Минимум восемь символов, минимум одна буква и одна цифра.')
        return value


class UserData(BaseModel):
    """Схема изменения данных пользователя."""
    username: str | None


class UserRole(BaseModel):
    """Схема проверки прав пользователя."""
    role: str


class Role(BaseModel):
    """Схема роли."""

    label: RoleType


class RoleRepresentation(BaseModel):
    """Схема роли для представления."""

    id: UUID
    label: str


class AccountHistory(BaseModel):
    """Схема истории входов."""

    id: UUID
    created: datetime.datetime


class Pagination(BaseModel):
    """Схема пагинации."""

    page: int = current_app.config['PAGE']
    per_page: int = current_app.config['PER_PAGE']
