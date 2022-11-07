from http import HTTPStatus

test_data_for_change_password_successfull = [
    (
        {'username': 'oleg'},
        {
            'old_password': 'Ldfj78!ksjd',
            'new_password': 'tedsvsd1A'
        },
        {'msg': 'Successful password change'},
        {'status': HTTPStatus.OK},
    ),
    (
        {'username': 'liza'},
        {
            'old_password': 'lizaLi123!',
            'new_password': 'tedsvsd1A'
        },
        {'msg': 'Successful password change'},
        {'status': HTTPStatus.OK},
    ),
]

test_data_for_change_password_fail = [
    (
        {'username': 'oleg'},
        {
            'old_password': 'Ldfj78!ksjdk',
            'new_password': 'tedsvsd1A'
        },
        {
            'msg': 'Invalid password'
        },
        {'status': HTTPStatus.UNAUTHORIZED},
    ),
    (
        {'username': 'liza'},
        {
            'old_password': 'LKjj78!ksjd',
            'new_password': 'tedsvsd1A'
        },
        {
            'msg': 'Invalid password'
        },
        {'status': HTTPStatus.UNAUTHORIZED},
    ),
    (
        {'username': 'oleg'},
        {
            'old_password': 'tedsvsd1A',
            'new_password': 'teds'
        },
        {
            'validation_error': {
                'body_params': [
                    {
                        'loc': [
                            'new_password'
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
        {'username': 'liza'},
        {
            'old_password': 'tedsvsd1A',
            'new_password': '123455667890'
        },
        {
            'validation_error': {
                'body_params': [
                    {
                        'loc': [
                            'new_password'
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
        {'username': 'liza'},
        {
            'old_password': 'tedsvsd1A',
            'ne_password': 'qwe123QWE'
        },
        {
            'validation_error': {
                'body_params': [
                    {
                        'loc': [
                            'new_password'
                        ],
                        'msg': 'field required',
                        'type': 'value_error.missing'
                    }
                ]
            }
        },
        {'status': HTTPStatus.BAD_REQUEST},
    ),
    (
        {'username': 'liza'},
        {
            'ol_password': 'tedsvsd1A',
            'new_password': 'qwe123QWE'
        },
        {
            'validation_error': {
                'body_params': [
                    {
                        'loc': [
                            'old_password'
                        ],
                        'msg': 'field required',
                        'type': 'value_error.missing'
                    }
                ]
            }
        },
        {'status': HTTPStatus.BAD_REQUEST},
    ),
    (
        {'username': 'liza'},
        {
            'ol_password': 'tedsvsd1A',
            'ne_password': 'qwe123QWE'
        },
        {
            'validation_error': {
                'body_params': [
                    {
                        'loc': [
                            'old_password'
                        ],
                        'msg': 'field required',
                        'type': 'value_error.missing'
                    },
                    {
                        'loc': [
                            'new_password'
                        ],
                        'msg': 'field required',
                        'type': 'value_error.missing'
                    }
                ]
            }
        },
        {'status': HTTPStatus.BAD_REQUEST},
    ),
]
