from flask import url_for
from core.oauth import get_oauth_instance
from services.json import JsonService
from services.auth import AuthService, get_auth_service
from api.v1.socials import auth_socials_v1
from models.general import SocialLoginType
from services.utils import info_from_mail

oauth = get_oauth_instance()


@auth_socials_v1.route('/mail/login')
def login_mail():
    redirect_uri = url_for('auth_socials_v1.auth_mail', _external=True)
    uri = oauth.mail.create_authorization_url(redirect_uri)
    oauth.mail.save_authorize_data(redirect_uri=redirect_uri, **uri)
    return JsonService.return_success_response(url=uri['url'])


@auth_socials_v1.route('/mail/callback')
def auth_mail():
    token = oauth.mail.authorize_access_token()
    response = oauth.mail.get('?access_token='+token['access_token'])
    email, social_id = info_from_mail(response)
    account = AuthService.get_user_social(social_id=social_id, social_name=SocialLoginType.MAIL.value)
    if not account:
        account = get_auth_service().create_oauth_user(
            email=email, social_id=social_id, social_name=SocialLoginType.MAIL.value
        )
    access_token, refresh_token = get_auth_service().create_tokens(account.user)
    get_auth_service().add_to_history(account.user)
    return JsonService.return_success_response(access_token=access_token, refresh_token=refresh_token)
