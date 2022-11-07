from http import HTTPStatus

test_data_for_success_login_user = [
    (
        {
            'username': 'ivan',
            'password': 'ivanivanov12IN!'
        },
        {'status': HTTPStatus.OK},
    ),
    (
        {
            'username': 'liza',
            'password': 'lizaLi123!'
        },
        {'status': HTTPStatus.OK},
    ),
]

test_data_for_unsuccess_login_user = [
    (
        {
            'username': 'ivanovivanov',
            'password': 'ivanivanov12IN!'
        },
        {'status': HTTPStatus.NOT_FOUND},
    ),
    (
        {
            'username': 'lizaliza',
            'password': 'ivanivanov'
        },
        {'status': HTTPStatus.NOT_FOUND},
    ),
]

test_data_for_not_exists_login_user = [
    (
        {
            'username': 'ivanovivanov',
            'password': 'ivanivanov12IN!'
        },
        {'status': HTTPStatus.NOT_FOUND},
        {'msg': 'User not found'}
    ),
    (
        {
            'username': 'lizaliza',
            'password': 'ivan231ivanov'
        },
        {'status': HTTPStatus.NOT_FOUND},
        {'msg': 'User not found'}
    ),
]

test_data_for_not_correct_password_login_user = [
    (
        {
            'username': 'ivan',
            'password': 'ivanivanov1dffdfdfdf2IN!'
        },
        {'status': HTTPStatus.UNAUTHORIZED},
        {'msg': 'Invalid password'}
    ),
    (
        {
            'username': 'liza',
            'password': 'lsKFSLkdmskdmfs'
        },
        {'status': HTTPStatus.UNAUTHORIZED},
        {'msg': 'Invalid password'}
    ),
]
