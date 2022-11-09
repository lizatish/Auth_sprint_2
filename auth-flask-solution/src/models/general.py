import enum


class RoleType(str, enum.Enum):
    """Тип роли пользователя."""

    STANDARD = 'standard'
    PRIVILEGED = 'privileged'
    ADMIN = 'admin'
    TEST = 'test'


class SocialLoginType(str, enum.Enum):
    """Типы социальных сетей."""

    GOOGLE = 'google'
    YANDEX = 'yandex'
    FACEBOOK = 'facebook'
    TWITTER = 'twitter'
