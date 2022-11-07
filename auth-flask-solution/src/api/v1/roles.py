from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_pydantic import validate

from api.v1.schemas import Role, RoleRepresentation
from decorators import admin_required
from services.auth import AuthService
from services.json import JsonService
from services.roles import RolesService, get_roles_service
from services.utils import is_valid_uuid

roles_v1 = Blueprint('roles_v1', __name__)


@roles_v1.route("/role", methods=["POST"])
@validate()
@jwt_required()
@admin_required
def roles_create(body: Role):
    """
    Создать новую роль
    ---
    tags:
      - Admin
    parameters:
      - name: body
        in: body
        required: true
        description: Новая роль
        schema:
          id: Role
          required:
            - name
          properties:
            label:
              type: string
              description: Название роли
      - in: header
        name: Authorization
        required: true
        description: Access-токен пользователя
        schema:
            type: string
    responses:
      200:
        description: Роль создана
        schema:
           id: RoleCreated
           properties:
              msg:
                type: string
                example: Role created!
      409:
        description: Роль уже существует
        schema:
           id: RoleExists
           properties:
              msg:
                type: string
                example: Role exists!
    """

    role = RolesService.get_role_by_label(body.label)
    if role:
        return JsonService.return_role_exists()
    get_roles_service().create_role(body.label)
    return JsonService.return_success_response(msg="Role created!")


@jwt_required()
@admin_required
@roles_v1.route("/role", methods=["GET"])
def roles_scope():
    """
    Получить список ролей
    ---
    tags:
      - Admin
    parameters:
      - in: header
        name: Authorization
        required: true
        description: Access-токен пользователя
        schema:
            type: string
    responses:
      200:
        description: Роль создана
        schema:
           id: RoleRepresentation
           properties:
              id:
                type: string
                description: Идентификатор роли
              label:
                type: string
                description: Название роли
    """
    roles = RolesService.get_roles()
    return JsonService.prepare_output(RoleRepresentation, roles)


@jwt_required()
@admin_required
@roles_v1.route("/role/<role_id>", methods=["GET"])
def role_retriew(role_id):
    """
    Получить данные о роли
    ---
    tags:
      - Admin
    parameters:
      - name: query
        in: query
        required: true
        description: Идентификатор роли
      - in: header
        name: Authorization
        required: true
        description: Access-токен пользователя
        schema:
            type: string
    responses:
      200:
        description: Роль создана
        schema:
           id: RoleRepresentation
           properties:
              id:
                type: string
                description: Идентификатор роли
              label:
                type: string
                description: Название роли
      422:
        description: Некорректный формат uuid
        schema:
           id: IncorrectUuid
           properties:
              msg:
                type: string
                example: Bad format uuid
      404:
        description: Роли не существует
        schema:
           id: RoleNotFound
           properties:
              msg:
                type: string
                example: Role not found
    """
    if not is_valid_uuid(role_id):
        return JsonService.return_uuid_fail()
    role = RolesService.get_role_by_id(role_id)
    if not role:
        return JsonService.return_role_not_found()
    return JsonService.prepare_single_output(RoleRepresentation, role)


@jwt_required()
@admin_required
@roles_v1.route("/role/<role_id>", methods=["DELETE"])
def role_delete(role_id):
    """
    Удалить роль
    ---
    tags:
      - Admin
    parameters:
      - name: query
        in: query
        required: true
        description: Идентификатор роли
      - in: header
        name: Authorization
        required: true
        description: Access-токен пользователя
        schema:
            type: string
    responses:
      200:
        description: Роль удалена
        schema:
          id: RoleDeleted
          properties:
             msg:
               type: string
               example: Role deleted!
      422:
        description: Некорректный формат uuid
        schema:
           id: IncorrectUuid
           properties:
              msg:
                type: string
                example: Bad format uuid
      404:
        description: Роли не существует
        schema:
           id: RoleNotFound
           properties:
              msg:
                type: string
                example: Role not found
    """
    if not is_valid_uuid(role_id):
        return JsonService.return_uuid_fail()
    deleted = get_roles_service().delete_role_by_id(role_id)
    if deleted:
        return JsonService.return_success_response(msg="Role deleted!")
    return JsonService.return_role_not_found()


@roles_v1.route("/role-manager/<user_id>", methods=["GET"])
@validate()
@jwt_required()
@admin_required
def role_appoint(user_id, query: Role):
    """
     Назначить роль пользователю
     ---
     tags:
       - Admin
     parameters:
       - name: user_id
         in: query
         required: true
         description: Идентификатор пользователя
       - name: role
         in: query
         required: true
         description: Название роли
         schema:
           id: Role
           properties:
              label:
                type: string
       - in: header
         name: Authorization
         required: true
         description: Access-токен пользователя
         schema:
             type: string
     responses:
       200:
         description: Роль удалена
         schema:
           id: RoleDeleted
           properties:
              msg:
                type: string
                example: Role deleted!
       422:
         description: Некорректный формат uuid
         schema:
            id: IncorrectUuid
            properties:
               msg:
                 type: string
                 example: Bad format uuid
       404:
         description: Роли не существует
         schema:
            id: RoleNotFound
            properties:
               msg:
                 type: string
                 example: Role not found
       404:
         description: Пользователя не существует
         schema:
            id: UserNotFound
            properties:
               msg:
                 type: string
                 example: Role not found
     """
    if not is_valid_uuid(user_id):
        return JsonService.return_uuid_fail()
    role = RolesService.get_role_by_label(query.label)
    if not role:
        return JsonService.return_role_not_found()
    user = AuthService.get_user_by_id(user_id)
    if not user:
        return JsonService.return_user_not_found()
    get_roles_service().change_user_role(role, user)
    return JsonService.return_success_response(msg="Role changed!")


@roles_v1.route("/role-manager/<user_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def role_take_away(user_id):
    """
     Назначить пользователю стандартную роль
     ---
     tags:
       - Admin
     parameters:
       - name: user_id
         in: query
         required: true
         description: Идентификатор пользователя
       - in: header
         name: Authorization
         required: true
         description: Access-токен пользователя
         schema:
             type: string
     responses:
       200:
         description: Роль пользователя назначена на стандартную
         schema:
           id: UserRoleToDefault
           properties:
              msg:
                type: string
                example: Role changed!
       422:
         description: Некорректный формат uuid
         schema:
            id: IncorrectUuid
            properties:
               msg:
                 type: string
                 example: Bad format uuid
       404:
         description: Пользователя не существует
         schema:
            id: UserNotFound
            properties:
               msg:
                 type: string
                 example: Role not found
     """
    if not is_valid_uuid(user_id):
        return JsonService.return_uuid_fail()
    user = AuthService.get_user_by_id(user_id)
    if not user:
        return JsonService.return_user_not_found()
    get_roles_service().change_user_role_to_default(user)
    return JsonService.return_success_response(msg="Role changed!")
