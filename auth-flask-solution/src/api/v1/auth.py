import uuid

from flask import Blueprint, request
from flask_jwt_extended import get_jwt, current_user, jwt_required
from flask_pydantic import validate
from pydantic import BaseModel

from api.v1.schemas import RefreshAccessTokensResponse, UserData, PasswordChange, UserRegistration
from api.v1.schemas import UserLoginScheme, AccountHistory, Pagination
from core.jwt import get_jwt_instance
from services.auth import AuthService, get_auth_service
from services.json import JsonService

auth_v1 = Blueprint('auth_v1', __name__)
jwt = get_jwt_instance()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """Проверка access-токена, что он не лежит уже в revoked-токенах."""
    jti_access_token = jwt_payload["jti"]

    user = AuthService.get_user_by_username(jwt_payload['sub']['username'])
    if not user:
        return JsonService.return_user_not_found()

    compare_access_tokens = get_auth_service().check_access_token_is_revoked(user.id, jti_access_token)
    return not compare_access_tokens


@auth_v1.route("/login", methods=["POST"])
@validate()
def login(body: UserLoginScheme) -> RefreshAccessTokensResponse:
    """
    Аутентификация пользователя.
    ---
    tags:
      - Authorization
    parameters:
      - name: body
        in: body
        required: true
        description: Логин и пароль пользователя
        schema:
          id: UserLoginScheme
          required:
            - name
          properties:
            username:
              type: string
              description: Имя пользователя
            password:
              type: string
              description: Пароль пользователя
    responses:
      200:
        description: Сгенерированные токены доступа
        schema:
           id: RefreshAccessTokensResponse
           properties:
            access_token:
              type: string
              description: Access-токен
            refresh_token:
              type: string
              description: Refresh-токен
      404:
        description: Пользователь с таким именем не найден
        schema:
           id: UserNotFound
           properties:
              msg:
                type: string
                example: User not found
      403:
        description: Неверный пароль
        schema:
           id: PasswordVerificationFailed
           properties:
              msg:
                type: string
                example: Invalid password
    """
    user = AuthService.get_user_by_username(body.username)
    if not user:
        return JsonService.return_user_not_found()

    if not user.check_password(body.password):
        return JsonService.return_password_verification_failed()

    access_token, refresh_token = get_auth_service().create_tokens(user)
    get_auth_service().add_to_history(user)

    return JsonService.return_success_response(access_token=access_token, refresh_token=refresh_token)


@auth_v1.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh() -> RefreshAccessTokensResponse:
    """
    Обновление access и refresh токена пользователя.
    ---
    tags:
      - Authorization
    parameters:
      - in: header
        name: Authorization
        required: true
        description: Refresh-токен пользователя
        schema:
            type: string
    responses:
      200:
        description: Сгенерированные токены доступа
        schema:
           id: RefreshAccessTokensResponse
           properties:
            access_token:
              type: string
              description: Access-токен
            refresh_token:
              type: string
              description: Refresh-токен
      404:
        description: Пользователя с таким именем не существует
        schema:
           id: UserNotFound
           properties:
              msg:
                type: string
                description: Пользователь не найден
                example: User not found
      403:
        description: Неверный пароль
        schema:
           id: RefreshTokenVerificationFailed
           properties:
              msg:
                type: string
                description: Неверный refresh-токен
                example: Invalid refresh token
    """
    refresh_token = JsonService.get_authorization_header_token(request)
    compare_refresh_tokens = get_auth_service().check_refresh_token(current_user.id, refresh_token)
    if not compare_refresh_tokens:
        return JsonService.return_invalid_refresh_token()

    access_token = get_jwt()["jti"]
    get_auth_service().set_revoked_access_token(current_user.id, access_token)

    access_token, refresh_token = get_auth_service().create_tokens(current_user)
    return JsonService.return_success_response(access_token=access_token, refresh_token=refresh_token)


@auth_v1.route("/registration", methods=["POST"])
@validate()
def registration(body: UserRegistration):
    """
    Регистрация пользователя.
    ---
    tags:
      - Authorization
    parameters:
      - name: body
        in: body
        required: true
        description: Логин и пароль пользователя
        schema:
          id: UserLoginScheme
          required:
            - name
          properties:
            username:
              type: string
              description: Имя пользователя
            password:
              type: string
              description: Пароль пользователя
    responses:
      200:
        description: Регистрация прошла успешно
        schema:
           id: SuccessfulRegistration
           properties:
             msg:
               type: string
               example: Successful registration
      400:
        description: Ошибка валидации пароля
        schema:
           id: PasswordValidationFailed
           properties:
             msg:
               type: string
               example: The password must contain at least eight characters, at least one letter and one number.
      409:
        description: Пользователь с таким именем уже существует
        schema:
           id: UserAlreadyExists
           properties:
              msg:
               type: string
               example: User with this username already exists!
    """
    user = AuthService.get_user_by_username(body.username)
    if user:
        return JsonService.return_user_exists()
    get_auth_service().create_user(body.username, body.password, body.email)
    return JsonService.return_success_response(msg='Successful registration')


@auth_v1.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Разлогинить пользователя.
    ---
    tags:
      - Authorization
    parameters:
      - in: header
        name: Authorization
        required: true
        description: Access-токен пользователя
        schema:
            type: string
    responses:
      200:
        description: Пользователь разлогинен
        schema:
           id: UserLoggedOut
           properties:
              msg:
                type: string
                example: User has been logged out
      404:
        description: Пользователя с таким именем не существует
        schema:
           id: UserNotFound
           properties:
              msg:
                type: string
                description: Пользователь не найден
                example: User not found
    """
    access_token = get_jwt()["jti"]
    get_auth_service().logout_user(current_user.id, access_token)

    return JsonService.return_success_response(msg="User has been logged out")


@auth_v1.route("/password-change", methods=["POST"])
@validate()
@jwt_required()
def password_change(body: PasswordChange):
    """
    Изменение пароля пользователя
    ---
    tags:
      - Data Change
    parameters:
      - in: header
        name: Authorization
        required: true
        description: Access-токен пользователя
        schema:
            type: string
      - in: body
        name: body
        required: true
        description: Старый и новый пароли пользователя
        schema:
          id: PasswordChange
          required:
            - name
          properties:
            old_password:
              type: string
              description: Старый пароль пользователя
            new_password:
              type: string
              description: Новый пароль пользователя
    responses:
      200:
        description: Смена пароля прошла успешно
        schema:
           id: SuccessPasswordChange
           properties:
             msg:
               type: string
               example: Successful password change
      400:
       description: Ошибка валидации пароля
       schema:
          id: PasswordValidationFailed
          properties:
             msg:
               type: string
               example: The password must contain at least eight characters, at least one letter and one number.
      403:
        description: Неверный пароль
        schema:
           id: PasswordVerificationFailed
           properties:
              msg:
                type: string
                example: Invalid password
      404:
        description: Пользователь с таким именем не найден
        schema:
           id: UserNotFound
           properties:
              msg:
                type: string
                example: User not found
    """
    if not current_user.check_password(body.old_password):
        return JsonService.return_password_verification_failed()
    get_auth_service().change_password(current_user, body.new_password)
    return JsonService.return_success_response(msg='Successful password change')


@auth_v1.route("/user", methods=["PUT"])
@validate()
@jwt_required()
def change_user_data(body: UserData):
    """
    Изменение данных пользователя
    ---
    tags:
      - Data Change
    parameters:
      - in: header
        name: Authorization
        required: true
        description: Access-токен пользователя
        schema:
            type: string
      - in: body
        name: body
        required: true
        description: Новые данные пользователя
        schema:
          id: UserData
          required:
            - name
          properties:
            username:
              type: string
              description: Новое имя пользователя
    responses:
      200:
        description: Смена данных пользователя прошла успешно
        schema:
           id: SuccessUserDataChange
           properties:
             msg:
               type: string
               example: Successful user data changed
      404:
        description: Пользователь с таким именем не найден
        schema:
           id: UserNotFound
           properties:
              msg:
                type: string
                example: User not found
      409:
        description: Пользователь с таким именем уже существует
        schema:
           id: UserAlreadyExists
           properties:
              msg:
               type: string
               example: User with this username already exists!
    """
    created = get_auth_service().change_user_data(current_user, body)
    if not created:
        return JsonService.return_user_exists()
    return JsonService.return_success_response(msg='Successful user data changed')


@auth_v1.route("/account-history", methods=["GET"])
@validate()
@jwt_required()
def account_history(query: Pagination):
    """
    Выводит историю входов аккаунта.
    ---
    tags:
      - User account
    parameters:
      - in: header
        name: Authorization
        required: true
        description: Access-токен пользователя
        schema:
            type: string
    responses:
      200:
        description: История входа для данного аккаунта
        schema:
           id: AccountHistory
           properties:
            user_id:
              type: str
              description: Идентификатор пользователя
            created:
              type: datetime
              description: Время входа
      404:
        description: Пользователь с таким именем не найден
        schema:
           id: UserNotFound
           properties:
              msg:
                type: string
                example: User not found
    """
    account_history_data = get_auth_service().get_account_history(
        current_user, query.page, query.per_page
    )

    prepared_output = JsonService.prepare_output(AccountHistory, account_history_data.items)
    return JsonService.pagination_return(account_history_data, prepared_output)


class UserProtectedData(BaseModel):
    role: str
    user_id: uuid.UUID


@auth_v1.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """
    Проверяет и возвращает роль пользователя
    ---
    tags:
      - Authorization
    parameters:
      - in: header
        name: Authorization
        required: true
        description: Access-токен пользователя
        schema:
            type: string
    responses:
      200:
        description: Роль пользвателя
        schema:
           id: UserRole
           properties:
             properties:
              msg:
                type: string
                example: [ADMIN, STANDARD, PRIVILEGED]
    """
    return JsonService.return_success_response(
        **UserProtectedData(
            role=current_user.role.label.name,
            user_id=current_user.id,
        ).dict())


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    Делает переменную current_user доступной в каждой конечной точке с помощью @jwt_required
    """
    identity = jwt_data['sub']
    return AuthService.get_user_by_username(identity['username'])
