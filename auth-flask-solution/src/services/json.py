from http import HTTPStatus
import orjson
from flask import jsonify, Request


class JsonService:
    @staticmethod
    def return_user_not_found():
        """Возвращает ответ пользователю, если пользователь не найден."""
        return {"msg": "User not found"}, HTTPStatus.NOT_FOUND

    @staticmethod
    def return_role_not_found():
        """Возвращает ответ пользователю, если роль не найдена."""
        return {"msg": "Role not found"}, HTTPStatus.NOT_FOUND

    @staticmethod
    def return_uuid_fail():
        """Возвращает ответ пользователю, если id неверный."""
        return {"msg": "Bad format uuid"}, HTTPStatus.UNPROCESSABLE_ENTITY

    @staticmethod
    def return_password_verification_failed():
        """Возвращает ответ пользователю, если введенный пароль не верен."""
        return {"msg": "Invalid password"}, HTTPStatus.UNAUTHORIZED

    @staticmethod
    def return_success_response(**kwargs):
        """Возвращает ответ пользователю,сообщающий о выполнении успешной операции."""
        return jsonify(**kwargs)

    @staticmethod
    def return_invalid_refresh_token():
        """Возвращает невалидный refresh-токен."""
        return {"msg": "Invalid refresh token"}, HTTPStatus.UNAUTHORIZED

    @staticmethod
    def get_refresh_token(request: Request):
        """Возвращает refresh-token из заголовка запроса."""
        headers = request.headers
        bearer = headers.get('Authorization')
        return bearer.split()[1]

    @staticmethod
    def return_user_exists():
        """Возвращает ответ пользователю, если такой логин уже используется."""
        return {"msg": "User with this username already exists!"}, HTTPStatus.CONFLICT

    @staticmethod
    def return_role_exists(**kwargs):
        """Возвращает ответ пользователю,сообщающий о выполнении успешной операции."""
        return {"msg": "Role exists!"}, HTTPStatus.CONFLICT

    @staticmethod
    def prepare_output(model, items):
        """Возвращает данные в json формате приведенные к нужной модели."""
        return [orjson.loads(model(**item.__dict__).json()) for item in items]

    @staticmethod
    def pagination_return(paginator, data):
        """Возвращает данные с информацией о пагинации."""
        return {
            'page': paginator.page,
            'pages': paginator.pages,
            'total_count': paginator.total,
            'prev_page': paginator.prev_num,
            'next_page': paginator.next_num,
            'has_next': paginator.has_next,
            'has_prev': paginator.has_prev,
            'results': data
        }

    @staticmethod
    def prepare_single_output(model, item):
        """Возвращает данные в json формате приведенные к нужной модели."""
        return orjson.loads(model(**item.__dict__).json())

    @staticmethod
    def get_authorization_header_token(request: Request):
        """Возвращает токен из заголовка запроса."""
        headers = request.headers
        bearer = headers.get('Authorization')
        return bearer.split()[1]

    @staticmethod
    def return_admins_only():
        """Возвращает ответ, если доступ производится не из-под требуемого админского аккаунта."""
        return {"msg": "Admins only!"}, HTTPStatus.FORBIDDEN
