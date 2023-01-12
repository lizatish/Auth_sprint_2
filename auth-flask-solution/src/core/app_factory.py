from flasgger import Swagger
from flask import Flask, request
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from core.cache import create_cache
from core.jwt import create_jwt
from core.limiter import create_limiter
from core.oauth import create_oauth
from core.tracer import configure_tracer
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
    create_limiter(app)
    Swagger(app)
    if app.config['ENABLE_TRACER']:
        configure_tracer()
        FlaskInstrumentor().instrument_app(app)

    # Регистрация отдельных компонентов (API)
    from api.v1.auth import auth_v1
    from api.v1.roles import roles_v1
    from api.v1.socials import auth_socials_v1
    from api.v1.users import users_v1
    from core.commands import usersbp

    app.register_blueprint(usersbp)
    app.register_blueprint(auth_v1, url_prefix='/auth/v1/users/')
    app.register_blueprint(roles_v1, url_prefix='/auth/v1/roles/')
    app.register_blueprint(auth_socials_v1, url_prefix='/auth/v1/oauth/')
    app.register_blueprint(users_v1, url_prefix='/protected/v1/users/')

    if app.config['ENABLE_TRACER']:
        @app.before_request
        def before_request():
            request_id = request.headers.get('X-Request-Id')
            if not request_id:
                raise RuntimeError('Request id is required')

    return app
