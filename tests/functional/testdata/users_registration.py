from http import HTTPStatus

test_data_for_registration_successfull = [
    (
        {
            'username': 'test27',
            'password': 'test8Anadssf'
        },
        {'msg': 'Successful registration'},
        {'status': HTTPStatus.OK},
    ),
    (
        {
            'username': 'test',
            'password': 'qwe1Er23'
        },
        {'msg': 'Successful registration'},
        {'status': HTTPStatus.OK},
    ),
]

test_data_for_registration_fail = [
    (
        {
            'username': 'test28',
            'password': 'test8Anadssf'
        },
        {
            'msg': 'User with this username already exists!'
        },
        {'status': HTTPStatus.CONFLICT},
    ),
    (
        {
            'username': 'test29',
            'password': 'test8Anadssf'
        },
        {
            'msg': 'User with this username already exists!'
        },
        {'status': HTTPStatus.CONFLICT},
    ),
    (
        {
            'username': 'test29',
            'password': 'test'
        },
        {
            'validation_error': {
                'body_params': [
                    {
                        'loc': [
                            'password'
                        ],
                        'msg': 'Минимум восемь символов, минимум одна буква и одна цифра.',
                        'type': 'value_error'
                    }
                ]
            }
        },
        {'status': HTTPStatus.BAD_REQUEST},
    ),
    (
        {
            'username': 'test29',
            'password': 'qwertyuio'
        },
        {
            'validation_error': {
                'body_params': [
                    {
                        'loc': [
                            'password'
                        ],
                        'msg': 'Минимум восемь символов, минимум одна буква и одна цифра.',
                        'type': 'value_error'
                    }
                ]
            }
        },
        {'status': HTTPStatus.BAD_REQUEST},
    ),
]
