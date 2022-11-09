from flask import url_for
from core.oauth import get_oauth_instance
from services.json import JsonService
from services.auth import AuthService, get_auth_service
from api.v1.socials import auth_socials_v1
from models.general import SocialLoginType
from services.utils import info_from_facebook

oauth = get_oauth_instance()


@auth_socials_v1.route('/facebook/login')
def login_facebook():
    redirect_uri = url_for('auth_socials_v1.auth_facebook', _external=True)
    uri = oauth.facebook.create_authorization_url(redirect_uri)
    oauth.facebook.save_authorize_data(redirect_uri=redirect_uri, **uri)
    return JsonService.return_success_response(url=uri['url'])


@auth_socials_v1.route('/facebook/callback')
def auth_facebook():
    oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get('/me?fields=id,email')
    email, social_id = info_from_facebook(resp)
    account = AuthService.get_user_social(social_id=social_id, social_name=SocialLoginType.FACEBOOK.value)
    if not account:
        account = get_auth_service().create_oauth_user(
            email=email, social_id=social_id, social_name=SocialLoginType.FACEBOOK.value
        )
    access_token, refresh_token = get_auth_service().create_tokens(account.user)
    get_auth_service().add_to_history(account.user)
    return JsonService.return_success_response(access_token=access_token, refresh_token=refresh_token)
