from werkzeug.security import generate_password_hash, check_password_hash

from tests.functional.settings import get_settings

conf = get_settings()


def hash_password(password: str):
    return generate_password_hash(
        password,
        method=conf.AUTH_HASH_METHOD,
        salt_length=conf.AUTH_HASH_SALT_LENGTH,
    )


def compare_password_hash(password_hash: str, password: str):
    return check_password_hash(password_hash, password)
