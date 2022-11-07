import enum


class RoleType(str, enum.Enum):
    """Тип роли пользователя."""

    STANDARD = 'standard'
    PRIVILEGED = 'privileged'
    ADMIN = 'admin'
    TEST = 'test'
