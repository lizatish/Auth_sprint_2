from flask import Flask
from authlib.integrations.flask_client import OAuth

oauth: OAuth | None = None


def create_oauth(app: Flask):
    """Инициализирует oauth."""
    global oauth
    with app.app_context():
        oauth = OAuth(app)
        oauth.register(
            name='google',
            server_metadata_url=app.config['GOOGLE_CLIENT_CONF_URL'],
            client_kwargs={
                'scope': 'openid email profile'
            }
        )


def get_oauth_instance() -> OAuth:
    """Возвращает экземпляр oauth."""
    return oauth
