from http import HTTPStatus

from models.general import RoleType

test_data_protected_access = [
    (
        {
            'username': 'ivan',
            'role': RoleType.STANDARD.name
        },
        {'status': HTTPStatus.OK},
        {'msg': 'STANDARD'}
    ),
    (
        {
            'username': 'admin',
            'role': RoleType.ADMIN.name
        },
        {'status': HTTPStatus.OK},
        {'msg': 'ADMIN'}
    )
]


test_data_protected_admin_access_only_successed = [
    (
        {
            'id': 'e2da75c0-8f07-4d20-bfc4-8afcf58e7a2c',
            'username': 'admin',
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY},
        {"msg": "Bad format uuid"},
    )
]
test_data_protected_admin_access_only_failed = [
    (
        {
            'id': '16bdbb16-d3bf-4184-b08e-e2b2eabeee7f',
            'username': 'ivan',
        },
        {'status': HTTPStatus.FORBIDDEN},
        {"msg": "Admins only!"}
    ),
]
