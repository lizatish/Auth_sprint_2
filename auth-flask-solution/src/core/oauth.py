from authlib.integrations.flask_client import OAuth
from flask import Flask

oauth: OAuth | None = None


def create_oauth(app: Flask):
    """Инициализирует oauth."""
    global oauth
    with app.app_context():
        oauth = OAuth(app)
        oauth.register(name='google')
        oauth.register(name='facebook')
        oauth.register(name='yandex')
        oauth.register(name='twitter')
        oauth.register(name='vk')
        oauth.register(name='mail')


def get_oauth_instance() -> OAuth:
    """Возвращает экземпляр oauth."""
    return oauth
