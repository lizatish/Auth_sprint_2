from functools import lru_cache
import uuid

from flask_jwt_extended import create_access_token, create_refresh_token

from db.cache import CacheStorage
from db.redis import get_redis_storage
from models.db_models import User, Role, db, AccountHistory, SocialAccount
from models.general import RoleType
from services.cache import CacheService
from services.utils import get_or_create


class AuthService:
    """Сервис авторизации и аутентификации."""

    def __init__(self, cache_storage: CacheStorage):
        """Инициализация сервиса."""
        self.cache_service = CacheService(cache_storage)
        self.db_connection = db

    def update_refresh_token(self, user_id: str, refresh_token: str):
        """Обновить refresh-токен."""
        self.cache_service.set_refresh_token(user_id, refresh_token)

    def add_to_history(self, user):
        """Добавить историю входа."""
        history = AccountHistory(user=user)
        self.db_connection.session.add(history)
        self.db_connection.session.commit()

    def get_account_history(self, user: User, page: int, per_page: int):
        """Получить историю входов с пагинацией."""
        return AccountHistory.query.filter_by(user=user).paginate(page=page, per_page=per_page)

    def create_tokens(self, user: User):
        """Создать access и refresh токены для пользователя."""
        token_user_data = {"username": user.username, "role": user.role.label.name}
        access_token = create_access_token(identity=token_user_data)
        refresh_token = create_refresh_token(identity=token_user_data)

        self.update_refresh_token(user_id=user.id, refresh_token=refresh_token)

        return access_token, refresh_token

    def update_revoked_access_token(self, user_id: str, revoked_access_token: str):
        """Обновить access-токен."""
        self.cache_service.set_revoked_access_token(user_id, revoked_access_token)

    def check_refresh_token(self, user_id: str, refresh_token: str) -> bool:
        """Сравнивает refresh-токен с тем, что лежит в redis."""
        current_refresh_token = self.cache_service.get_refresh_token(user_id)
        if current_refresh_token.decode('ascii') == refresh_token:
            return True
        return False

    def create_user(self, username: str, password: str):
        """Создать пользователя."""
        role = get_or_create(self.db_connection.session, Role, label=RoleType.STANDARD)
        user = User(username=username, role=role)
        user.set_password(password)
        self.db_connection.session.add(user)
        self.db_connection.session.commit()

    def create_oauth_user(self, social_id: str, social_name: str, email: str, username: str = None):
        """Создать пользователя и социальный аккаунт."""
        role = get_or_create(self.db_connection.session, Role, label=RoleType.STANDARD)
        if not username:
            username = email.split('@')[0]
        user = User(username=username, role=role, email=email)
        password = uuid.uuid4().hex.upper()[0:8]
        user.set_password(password)
        self.db_connection.session.add(user)
        self.db_connection.session.commit()
        social = SocialAccount(social_name=social_name, social_id=social_id, user=user)
        self.db_connection.session.add(social)
        self.db_connection.session.commit()
        return social

    def create_superuser(self, username: str, password: str):
        """Создать супер-пользователя."""
        role = get_or_create(self.db_connection.session, Role, label=RoleType.ADMIN)
        user = User(username=username, role=role)
        user.set_password(password)
        self.db_connection.session.add(user)
        self.db_connection.session.commit()

    def change_password(self, user, password: str):
        """Поменять пароль."""
        user.set_password(password)
        self.db_connection.session.commit()

    def change_user_data(self, user, body):
        """Поменять данные пользователя."""
        if (body.username) and (body.username != user.username):
            if not self.get_user_by_username(body.username):
                user.username = body.username
            else:
                return False
        self.db_connection.session.commit()
        return True

    def logout_user(self, user_id: str, revoked_access_token: str):
        """Разлогинивает пользователя."""
        self.cache_service.set_revoked_access_token(user_id, revoked_access_token)
        self.cache_service.delete_refresh_token(user_id)

    def set_revoked_access_token(self, user_id: str, revoked_access_token: str):
        """Помечает access-токен как отозванный."""
        self.cache_service.set_revoked_access_token(user_id, revoked_access_token)

    def check_access_token_is_revoked(self, user_id: str, access_token: str) -> bool:
        """Проверяет валидный access-токен на то, что он не лежит в базе отозванных токенов."""
        revokes_access_tokens_bin = self.cache_service.get_revoked_access_token(user_id)
        revokes_access_tokens = [token.decode('ascii') for token in revokes_access_tokens_bin]
        if access_token in revokes_access_tokens:
            return False
        return True

    @staticmethod
    def get_user_by_username(username: str) -> User:
        """Получить пользователя по его username."""
        return User.query.filter_by(username=username).one_or_none()

    @staticmethod
    def get_user_social(social_id: str, social_name: str) -> SocialAccount:
        """Получить социальный аккаунт."""
        return SocialAccount.query.filter_by(social_id=social_id, social_name=social_name).one_or_none()

    @staticmethod
    def get_user_by_id(user_id: str):
        """Получить пользователя по его id."""
        return User.query.get(user_id)


@lru_cache()
def get_auth_service() -> AuthService:
    """Возвращает экземпляр сервиса для работы с кинопроизведениями."""
    cache_storage: CacheStorage = get_redis_storage()
    return AuthService(cache_storage)
