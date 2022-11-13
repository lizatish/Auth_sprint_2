import json
import uuid

from core.oauth import get_oauth_instance

oauth = get_oauth_instance()


def is_valid_uuid(val):
    """Проверяет на валидность UUID."""
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def get_or_create(session, model, **kwargs):
    """Возвращает объект модели если он существует или создаёт новый."""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def get_userdata_from_google() -> dict:
    """Возвращает email и id пользователя, извлеченные из гугл токена."""
    token = oauth.twitter.authorize_access_token()
    return {'email': token['userinfo']['email'], 'social_id': token['userinfo']['sub']}


def get_userdata_from_facebook() -> dict:
    """Возвращает email и id пользователя, извлеченные из данных от facebook."""
    oauth.facebook.authorize_access_token()
    profile = oauth.facebook.get('/me?fields=id,email').json()
    return {'email': profile['email'], 'social_id': profile['id']}


def get_userdata_from_yandex() -> dict:
    """Возвращает email и id пользователя, извлеченные из данных от yandex."""
    oauth.yandex.authorize_access_token()
    user_data_response = oauth.yandex.get('info')
    user_data = json.loads(user_data_response.content)
    return {'email': user_data['default_email'], 'social_id': user_data['id']}


def get_userdata_from_twitter() -> dict:
    """Возвращает username и id пользователя, извлеченные из twitter токена."""
    token = oauth.twitter.authorize_access_token()
    return {'username': token['user_id'], 'social_id': token['screen_name']}
