from http import HTTPStatus

test_data_for_get_account_history = [
    (
        {
            'username': 'ivan',
            'password': 'ivanivanov12IN!'
        },
        {'status': HTTPStatus.OK, 'len': 1},
    ),
    (
        {
            'username': 'liza',
            'password': 'lizaLi123!'
        },
        {'status': HTTPStatus.OK, 'len': 1},
    ),
]
