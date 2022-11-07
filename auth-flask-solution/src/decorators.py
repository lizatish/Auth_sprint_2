from functools import wraps

from flask_jwt_extended import current_user

from models.general import RoleType
from services.json import JsonService


def admin_required(fn):
    """Проверяет доступ только для администратора."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.role.label.name != RoleType.ADMIN.name:
            return JsonService().return_admins_only()
        return fn(*args, **kwargs)

    return wrapper
