import click
import logging

from flask import Blueprint
from services.auth import get_auth_service, AuthService

usersbp = Blueprint('users', __name__)
logger = logging.getLogger(__name__)


@usersbp.cli.command('createsuperuser')
@click.argument('username')
@click.argument('password')
def createsuperuser(username, password):
    """
    Комадна для создания суперпользователя.
    На вход принимает логин и пароль.

    Пример: flask users createsuperuser admin qwe123QWE

    """
    user = AuthService.get_user_by_username(username)
    if user:
        return logger.warning(f"{username} - this username is already in use.")
    get_auth_service().create_superuser(username, password)
    return logger.warning(f"Created superuser: {username}")
