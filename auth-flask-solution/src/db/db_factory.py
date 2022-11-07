from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db: SQLAlchemy | None = None


def create_db(app: Flask):
    """Инициализирует бд для алхимии."""
    global db
    db = SQLAlchemy(app)
    Migrate(app, db)


def get_db() -> SQLAlchemy:
    """Возвращает экземпляр алхимии."""
    return db
