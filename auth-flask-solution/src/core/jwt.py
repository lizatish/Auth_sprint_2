from flask import Flask
from flask_jwt_extended import JWTManager

jwt: JWTManager | None = None


def create_jwt(app: Flask):
    """Инициализирует jwt."""
    global jwt
    with app.app_context():
        jwt = JWTManager(app)


def get_jwt_instance() -> JWTManager:
    """Возвращает экземпляр jwt."""
    return jwt
