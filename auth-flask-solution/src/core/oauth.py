from flask import Flask
from authlib.integrations.flask_client import OAuth

oauth: OAuth | None = None


def create_oauth(app: Flask):
    """Инициализирует oauth."""
    global oauth
    with app.app_context():
        oauth = OAuth(app)
        oauth.register(name='google')
        oauth.register(name='facebook')

def get_oauth_instance() -> OAuth:
    """Возвращает экземпляр oauth."""
    return oauth
