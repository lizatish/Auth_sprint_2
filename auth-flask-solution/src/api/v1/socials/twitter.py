from flask import url_for

from api.v1.socials import auth_socials_v1
from core.oauth import get_oauth_instance
from models.general import SocialLoginType
from services.auth import AuthService, get_auth_service
from services.json import JsonService
from services.utils import info_from_twitter

oauth = get_oauth_instance()


@auth_socials_v1.route('/twitter/login')
def login_twitter():
    """Аутентификация пользователя через twitter."""
    redirect_uri = url_for('auth_socials_v1.auth_twitter', _external=True)
    uri = oauth.twitter.create_authorization_url(redirect_uri)
    oauth.twitter.save_authorize_data(redirect_uri=redirect_uri, **uri)
    return JsonService.return_success_response(url=uri['url'])


@auth_socials_v1.route('/twitter/callback')
def auth_twitter():
    """Функция обратного вызова для аутентификации пользователя через twitter."""
    token = oauth.twitter.authorize_access_token()
    social_id, username = info_from_twitter(token)
    account = AuthService.get_user_social(social_id=social_id, social_name=SocialLoginType.TWITTER.value)
    if not account:
        account = get_auth_service().create_oauth_user(
            social_id=social_id, social_name=SocialLoginType.TWITTER.value, username=username
        )
    access_token, refresh_token = get_auth_service().create_tokens(account.user)
    get_auth_service().add_to_history(account.user)
    return JsonService.return_success_response(access_token=access_token, refresh_token=refresh_token)
