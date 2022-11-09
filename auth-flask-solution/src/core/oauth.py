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

        oauth.register(
            name='facebook',
            client_id=app.config['FACEBOOK_CLIENT_ID'],
            client_secret=app.config['FACEBOOK_CLIENT_SECRET'],
            access_token_url='https://graph.facebook.com/oauth/access_token',
            access_token_params=None,
            authorize_url='https://www.facebook.com/dialog/oauth',
            authorize_params=None,
            api_base_url='https://graph.facebook.com/',
            client_kwargs={'scope': 'email'},
        )

def get_oauth_instance() -> OAuth:
    """Возвращает экземпляр oauth."""
    return oauth
