from flask import url_for

from api.v1.socials import auth_socials_v1
from core.oauth import get_oauth_instance
from models.general import SocialLoginType
from services.auth import AuthService, get_auth_service
from services.json import JsonService
from services.utils import info_from_vk

oauth = get_oauth_instance()


@auth_socials_v1.route('/vk/login')
def vk_login():
    """Аутентификация пользователя через vkontakte."""
    redirect_uri = url_for('auth_socials_v1.vk_auth', _external=True)
    uri = oauth.vk.create_authorization_url(redirect_uri)
    oauth.vk.save_authorize_data(redirect_uri=redirect_uri, **uri)
    return JsonService.return_success_response(url=uri['url'])


@auth_socials_v1.route('/vk/callback')
def vk_auth():
    """Функция обратного вызова для аутентификации пользователя через yandex."""
    oauth.vk.authorize_access_token()
    user_data_response = oauth.vk.get('info')
    email, social_id = info_from_vk(user_data_response)
    account = AuthService.get_user_social(social_id=social_id, social_name=SocialLoginType.VK.value)

    if not account:
        account = get_auth_service().create_oauth_user(
            email=email,
            social_id=social_id,
            social_name=SocialLoginType.VK.value,
        )
    access_token, refresh_token = get_auth_service().create_tokens(account.user)
    get_auth_service().add_to_history(account.user)
    return JsonService.return_success_response(access_token=access_token, refresh_token=refresh_token)
