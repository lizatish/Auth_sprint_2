import uuid

from flask import Blueprint
from flask_pydantic import validate
from flask_jwt_extended import jwt_required

from api.v1.schemas import User, Pagination
from decorators import admin_required
from services.auth import get_auth_service
from services.json import JsonService
from services.utils import is_valid_uuid


users_v1 = Blueprint('users_v1', __name__)


@users_v1.route("/", methods=["GET"])
@validate()
@jwt_required()
@admin_required
def scope_users(query: Pagination):
    users = get_auth_service().get_users(
        query.page, query.per_page,
    )
    prepared_output = JsonService.prepare_output(User, users.items)
    return JsonService.pagination_return(users, prepared_output)


@users_v1.route("/<user_id>", methods=["GET"])
@jwt_required()
@admin_required
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
