import uuid

from flask import Blueprint, request
from flask_jwt_extended import get_jwt, current_user, jwt_required
from flask_pydantic import validate
from pydantic import BaseModel

from api.v1.schemas import RefreshAccessTokensResponse, UserData, PasswordChange, UserRegistration
from api.v1.schemas import User, AccountHistory, Pagination
from core.jwt import get_jwt_instance
from services.auth import AuthService, get_auth_service
from services.json import JsonService
from services.utils import is_valid_uuid


users_v1 = Blueprint('users_v1', __name__)
jwt = get_jwt_instance()


@users_v1.route("/", methods=["GET"])
@validate()
def scope_users(query: Pagination):
    users = get_auth_service().get_users(
        query.page, query.per_page,
    )
    prepared_output = JsonService.prepare_output(User, users.items)
    return JsonService.pagination_return(users, prepared_output)


@users_v1.route("/<user_id>", methods=["GET"])
def protected(user_id: uuid.UUID):
    if not is_valid_uuid(user_id):
        return JsonService.return_uuid_fail()
    user = get_auth_service().get_user_by_id(user_id)
    if not user:
        return JsonService.return_user_not_found()
    return JsonService.return_success_response(
        **User(
            username=user.username,
            email=user.email,
            id=user.id
        ).dict())
