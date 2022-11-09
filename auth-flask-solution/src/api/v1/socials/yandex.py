from flask import url_for

from api.v1.socials import auth_socials_v1
from core.oauth import get_oauth_instance
from models.general import SocialLoginType
from services.auth import AuthService, get_auth_service
from services.json import JsonService
from services.utils import info_from_yandex

oauth = get_oauth_instance()


@auth_socials_v1.route('/yandex/login')
def yandex_login():
    """Аутентификация пользователя через yandex."""
    redirect_uri = url_for('auth_socials_v1.yandex_auth', _external=True)
    uri = oauth.yandex.create_authorization_url(redirect_uri)
    oauth.yandex.save_authorize_data(redirect_uri=redirect_uri, **uri)
    return JsonService.return_success_response(url=uri['url'])


@auth_socials_v1.route('/yandex/callback')
def yandex_auth():
    """Функция обратного вызова для аутентификации пользователя через yandex."""
    oauth.yandex.authorize_access_token()
    user_data_response = oauth.yandex.get('info')
    email, social_id = info_from_yandex(user_data_response)
    account = AuthService.get_user_social(social_id=social_id, social_name=SocialLoginType.YANDEX)

    if not account:
        account = get_auth_service().create_oauth_user(
            email=email,
            social_id=social_id,
            social_name=SocialLoginType.YANDEX,
        )
    access_token, refresh_token = get_auth_service().create_tokens(account.user)
    get_auth_service().add_to_history(account.user)
    return JsonService.return_success_response(access_token=access_token, refresh_token=refresh_token)
