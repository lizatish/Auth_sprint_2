import requests
import re
from http import HTTPStatus
from core.config import get_settings

conf = get_settings()

async def get_role_from_auth(token: str):
    try:
        response = requests.get(conf.AUTH_SERVICE_PROTECTED, headers={"Authorization": token})
        response_body = response.json()
        if response.status_code == HTTPStatus.OK:
            role = response_body['msg']
        else:
            raise Exception
    except:
        role = conf.DEFAULT_USER_ROLE
    return role

async def prepare_url(url):
    return re.sub(
        r'[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}',
        'None',
        url
    )
