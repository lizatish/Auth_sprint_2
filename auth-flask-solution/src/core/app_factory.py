from flasgger import Swagger
from flask import Flask

from core.jwt import create_jwt
from core.cache import create_cache
from core.oauth import create_oauth
from db.db_factory import create_db


def create_app(config_filename: object) -> Flask:
    """Фабрика создания приложения."""
    app = Flask(__name__)

    app.config.from_object(config_filename)
    app.app_context().push()
    # Инициализация БД
    create_db(app)
    create_cache(app)
    create_jwt(app)
    create_oauth(app)
    Swagger(app)

    # Регистрация отдельных компонентов (API)
    from api.v1.auth import auth_v1
    from api.v1.roles import roles_v1
    from api.v1.socials.google import auth_google_v1
    from core.commands import usersbp

    app.register_blueprint(usersbp)
    app.register_blueprint(auth_v1)
    app.register_blueprint(roles_v1)
    app.register_blueprint(auth_google_v1)
    return app
