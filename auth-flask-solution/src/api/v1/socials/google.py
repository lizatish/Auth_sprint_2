from flask import url_for
from core.oauth import get_oauth_instance
from services.json import JsonService
from services.auth import AuthService, get_auth_service
from api.v1.socials import auth_socials_v1

oauth = get_oauth_instance()


@auth_socials_v1.route('/google/login')
def login():
    redirect_uri = url_for('auth_socials_v1.auth_google', _external=True)
    uri = oauth.google.create_authorization_url(redirect_uri)
    oauth.google.save_authorize_data(redirect_uri=redirect_uri, **uri)
    return JsonService.return_success_response(url=uri['url'])


@auth_socials_v1.route('/google/callback')
def auth_google():
    token = oauth.google.authorize_access_token()
    email = token['userinfo']['email']
    social_id = token['userinfo']['sub']
    account = AuthService.get_user_social(social_id=social_id, social_name='google')
    if not account:
        account = get_auth_service().create_oauth_user(email=email, social_id=social_id, social_name='google')
    access_token, refresh_token = get_auth_service().create_tokens(account.user)
    get_auth_service().add_to_history(account.user)
    return JsonService.return_success_response(access_token=access_token, refresh_token=refresh_token)
