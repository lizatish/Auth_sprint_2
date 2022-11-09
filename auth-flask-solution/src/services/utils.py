import json
import uuid


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


def info_from_google_token(token):
    """Возвращает email и id пользователя, извлеченные из гугл токена."""
    return token['userinfo']['email'], token['userinfo']['sub']


def info_from_facebook(data):
    """Возвращает email и id пользователя, извлеченные из данных от facebook."""
    profile = data.json()
    return profile['email'], profile['id']


def info_from_yandex(user_data_response):
    """Возвращает email и id пользователя, извлеченные из данных от facebook."""
    user_data = json.loads(user_data_response.content)
    return user_data['default_email'], user_data['id']
