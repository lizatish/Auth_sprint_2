from functools import lru_cache

from flask import current_app

from models.db_models import User, db, Role
from services.utils import get_or_create


class RolesService:
    """Сервис ролей."""

    def __init__(self):
        """Инициализация сервиса."""
        self.db_connection = db

    @staticmethod
    def get_roles():
        """Получить все роли."""
        return Role.query.all()

    @staticmethod
    def get_role_by_id(role_id: str):
        """Получить роль по id"""
        return Role.query.get(role_id)

    def delete_role_by_id(self, role_id: str):
        """Удалить роль по id."""
        role = Role.query.get(role_id)
        if role:
            self.db_connection.session.delete(role)
            self.db_connection.session.commit()
            return True
        else:
            return False

    @staticmethod
    def get_role_by_label(label: str) -> User:
        """Получить роль по label."""
        return Role.query.filter_by(label=label).first()

    def create_role(self, label: str):
        """Создать роль."""
        role = Role(label=label)
        self.db_connection.session.add(role)
        self.db_connection.session.commit()

    def change_user_role(self, role, user):
        """Поменять права пользователя."""
        user.role = role
        self.db_connection.session.commit()

    def change_user_role_to_default(self, user):
        """Поменять права пользователя."""
        role = get_or_create(self.db_connection.session, Role, label=current_app.config['DEFAULT_ROLE_NAME'])
        user.role = role
        self.db_connection.session.commit()


@lru_cache()
def get_roles_service() -> RolesService:
    """Возвращает экземпляр сервиса для работы с кинопроизведениями."""
    return RolesService()
