from flask import Blueprint
from flask import url_for

from core.oauth import get_oauth_instance
from models.general import SocialLoginType
from services.auth import AuthService, get_auth_service
from services.json import JsonService
from services.utils import get_userdata_from_facebook, get_userdata_from_yandex, get_userdata_from_twitter, \
    get_userdata_from_google

auth_socials_v1 = Blueprint('auth_socials_v1', __name__)

oauth = get_oauth_instance()

socials_auth_mapping = {
    SocialLoginType.GOOGLE: get_userdata_from_google,
    SocialLoginType.YANDEX: get_userdata_from_yandex,
    SocialLoginType.TWITTER: get_userdata_from_twitter,
    SocialLoginType.FACEBOOK: get_userdata_from_facebook,
}


@auth_socials_v1.route('/<social_name>/login')
def socials_login(social_name: SocialLoginType):
    """Аутентификация через сторонние сервисы."""
    client = oauth.create_client(social_name)
    redirect_uri = url_for('auth_socials_v1.socials_auth', social_name=social_name, _external=True)
    uri = client.create_authorization_url(redirect_uri)
    client.save_authorize_data(redirect_uri=redirect_uri, **uri)
    return JsonService.return_success_response(url=uri['url'])


@auth_socials_v1.route('/<social_name>/callback')
def socials_auth(social_name: SocialLoginType):
    """Метод обратного вызова для аутентификации через сторонние сервисы."""
    prepared = SocialLoginType(social_name)
    user_data_kwargs = socials_auth_mapping[prepared]()

    account = AuthService.get_user_social(social_id=user_data_kwargs['social_id'], social_name=social_name)
    if not account:
        account = get_auth_service().create_oauth_user(**user_data_kwargs)
    access_token, refresh_token = get_auth_service().create_tokens(account.user)
    get_auth_service().add_to_history(account.user)
    return JsonService.return_success_response(access_token=access_token, refresh_token=refresh_token)
