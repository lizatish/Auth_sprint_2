import re
import uuid
import datetime
from typing import Optional

from flask import current_app
from sqlalchemy import ForeignKey, Enum, or_, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash

from db.db_factory import get_db
from models.general import RoleType


db = get_db()


class BaseMixin:
    """Миксин с базовыми методами для всех моделей."""

    @declared_attr
    def __tablename__(cls):
        """Подставляет snake_case как имя таблицы."""
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__.lower()).lower()


class UUIDMixin(BaseMixin):
    """Миксин с идентификатором моделей."""

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class Role(UUIDMixin, db.Model):
    """Модель пользователя."""

    label = db.Column(Enum(RoleType))
    users = db.relationship('User', backref='role')


class AccountHistory(UUIDMixin, db.Model):
    """Модель истории входов."""

    __table_args__ = (
        UniqueConstraint('id', 'created'),
        {
            'postgresql_partition_by': 'RANGE (created)',
        }
    )

    user_id = db.Column(UUID(as_uuid=True), ForeignKey("user.id"))
    created = db.Column(db.DateTime, default=datetime.datetime.now(), primary_key=True)


class User(UUIDMixin, db.Model):
    """Модель пользователя."""

    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=True)
    role_id = db.Column(UUID(as_uuid=True), ForeignKey("role.id"))
    password = db.Column(db.String(400), nullable=False)
    stories = db.relationship('AccountHistory', backref='user')

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def set_password(self, password: str):
        self.password = generate_password_hash(
            password,
            method=current_app.config['AUTH_HASH_METHOD'],
            salt_length=current_app.config['AUTH_HASH_SALT_LENGTH'],
        )

    @classmethod
    def get_user_by_universal_login(cls, username: Optional[str] = None, email: Optional[str] = None):
        """Возвращает пользователя по username или email, в зависимости от переданного значения."""
        return cls.query.filter(or_(cls.username == username, cls.email == email)).first()


class SocialAccount(UUIDMixin, db.Model):
    """Модель социальных аккаунтов."""

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, backref=db.backref('social_accounts', lazy=True))

    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint('social_id', 'social_name', name='social_pk'), )

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'
