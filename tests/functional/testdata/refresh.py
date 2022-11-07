from http import HTTPStatus

from models.general import RoleType

test_data_for_update_user_refresh_token = [
    (
        {
            'username': 'ivan',
            'password': 'ivanivanov'
        },
        {'status': HTTPStatus.OK},
    )
]

test_data_unsuccess_usage_old_refresh_token = [
    (
        {
            'username': 'ivan',
            'password': 'ivanivanov'
        },
        {'status': HTTPStatus.UNAUTHORIZED},
        {'msg': 'Invalid refresh token'}
    )
]

test_data_unsuccess_update_user_refresh_token_not_exists = [
    (
        {
            'username': 'not exists',
            'role': RoleType.STANDARD.name
        },
        {'status': HTTPStatus.UNAUTHORIZED},
        {'msg': 'Token has been revoked'}
    ),
    (
        {
            'username': 'ot exists2',
            'role': RoleType.ADMIN.name
        },
        {'status': HTTPStatus.UNAUTHORIZED},
        {'msg': 'Token has been revoked'},
    )
]

test_data_unsuccess_update_user_refresh_token_another_role = [
    (
        {
            'username': 'ivan',
            'role': RoleType.ADMIN.name
        },
        {'status': HTTPStatus.UNAUTHORIZED},
        {'msg': 'Invalid refresh token'}
    ),
    (
        {
            'username': 'admin',
            'role': RoleType.STANDARD.name
        },
        {'status': HTTPStatus.UNAUTHORIZED},
        {'msg': 'Invalid refresh token'}
    )
]
test_data_unsuccess_update_user_refresh_token_validation_error = [
    (
        'eyJhbGciOiJIvUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzI0MzI2MywianRpIj'
        'oiNzYyOGJmMDUtMDZhMi00NDA2LTgwZTAtMzc5NTU5YjYzN2YxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsidXNlcm5hbWU'
        'iOiJsaXphIiwicm9sZSI6InN0YW5kYXJkIn0sIm5iZiI6MTY2NzI0MzI2MywiZXhwIjoxNjY5ODM1MjYzfQ.OHA7JIAtza2pr'
        'avyhxv9n3UsZbqftKTd0uahPh8mkYc',
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY},
        {'msg': 'Invalid header padding'}
    ),
    (
        'e',
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY},
        {'msg': 'Not enough segments'}
    ),
    (
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzMxNjg5OSwianRpIjoi'
        'ODUwZmRkMGItYWM0OS00MGU1LWIwNzgtNmUzNzgwMGJhODMzIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsidXNlcm5hbWUiO'
        'iJsaXphIiwicm9sZSI6InN0YW5kYXJkIn0sIm5iZiI6MTY2NzMxNjg5OSwiZXhwIjoxNjY5OTA4ODk5fQ.w7icBrqVD5ANRAs'
        'oUPum5QahXv3zhErIpc-3rhExI4wvdfg',
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY},
        {'msg': 'Signature verification failed'}
    )
]
