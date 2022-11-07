from http import HTTPStatus

test_data_for_change_data_successfull = [
    (
        {
            'username': 'oleg',
            'id': 'bb81ead9-b728-461b-a0a9-eacc9b7127a2'
        },
        {
            "username": "test123"
        },
        {'msg': 'Successful user data changed'},
        {'status': HTTPStatus.OK},
    ),
]

test_data_for_change_data_fail = [
    (
        {'username': 'ivan'},
        {
            'username': 'liza'
        },
        {
            'msg': 'User with this username already exists!'
        },
        {'status': HTTPStatus.CONFLICT},
    ),
]
