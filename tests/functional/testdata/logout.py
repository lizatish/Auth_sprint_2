from http import HTTPStatus

from models.general import RoleType

test_data_for_test_success_logout = [
    (
        {
            'username': 'ivan',
            'role': RoleType.STANDARD.name
        },
        {'status': HTTPStatus.OK},
        {'msg': 'User has been logged out'}
    ),
    (
        {
            'username': 'admin',
            'role': RoleType.ADMIN.name
        },
        {'status': HTTPStatus.OK},
        {'msg': 'User has been logged out'}
    ),
]
test_data_for_test_failed_logout_token_revoked = [
    (
        {
            'username': 'ivan',
            'role': RoleType.STANDARD.name
        },
        {'status': HTTPStatus.UNAUTHORIZED},
        {'msg': 'Token has been revoked'}
    )
]

test_data_for_test_failed_logout_token_expired = [
    (
        {
            'username': 'ivan',
            'role': RoleType.STANDARD.name
        },
        {'status': HTTPStatus.UNAUTHORIZED},
        {'msg': 'Token has expired'}
    )
]
