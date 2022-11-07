from http import HTTPStatus


test_data_for_create_role_successful = [
    (
        {
            "label": "test",
        },
        {'msg': 'Role created!'},
        {'status': HTTPStatus.OK},
    ),
]


test_data_for_create_role_fail = [
    (
        {
            "label": "test2",
        },
        {
            "validation_error": {
                "body_params": [
                    {
                        "ctx": {
                            "enum_values": [
                                "standard",
                                "privileged",
                                "admin",
                                "test"
                            ]
                        },
                        "loc": [
                            "label"
                        ],
                        "msg": "value is not a valid enumeration member; "
                               "permitted: 'standard', 'privileged', 'admin', 'test'",
                        "type": "type_error.enum"
                    }
                ]
            }
        },
        {'status': HTTPStatus.BAD_REQUEST},
    ),
    (
        {
            "label": "admin",
        },
        {
            "msg": "Role exists!"
        },
        {'status': HTTPStatus.CONFLICT},
    ),
    (
        {
            "lael": "test",
        },
        {
            "validation_error": {
                "body_params": [
                    {
                        "loc": [
                            "label"
                        ],
                        "msg": "field required",
                        "type": "value_error.missing"
                    }
                ]
            }
        },
        {'status': HTTPStatus.BAD_REQUEST},
    ),
]


test_data_for_get_scope_roles = [
    (
        ['standard', 'privileged', 'admin', 'test'],
        {'status': HTTPStatus.OK, 'len': 4},
    ),
]


test_data_for_get_single_role = [
    (
        '815aa676-902d-4505-bbb5-42ca9727617f',
        {
            'id': '815aa676-902d-4505-bbb5-42ca9727617f',
            'label': 'standard'
        },
        {'status': HTTPStatus.OK},
    ),
    (
        'c07d6c8c-1d4f-4f54-b88f-2c2b962ad7b6',
        {
            'id': 'c07d6c8c-1d4f-4f54-b88f-2c2b962ad7b6',
            'label': 'admin'
        },
        {'status': HTTPStatus.OK},
    ),
]


test_data_for_get_single_role_fail = [
    (
        'qwe',
        {
            "msg": "Bad format uuid"
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY},
    ),
    (
        '16bdbb16-d3bf-4184-b08e-e2b2eabeee7f',
        {
            'msg': 'Role not found'
        },
        {'status': HTTPStatus.NOT_FOUND},
    ),
]


test_data_for_delete_role_fail = [
    (
        '16bdbb16-d3bf-4184-b08e-e2b2eabeee7f',
        {
            "msg": "Role not found"
        },
        {'status': HTTPStatus.NOT_FOUND},
    ),
    (
        'qwef',
        {
            "msg": "Bad format uuid"
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY},
    ),
]


test_data_for_delete_role = [
    (
        'c07d6c8c-1d4f-4f54-b88f-2c2b962ad7b6',
        {
            "msg": "Role deleted!"
        },
        {'status': HTTPStatus.OK},
    ),
]


test_data_for_role_appoint_successful = [
    (
        '15e794ed-2286-4690-b092-793f5e51f0ec',
        'privileged',
        {
            "msg": "Role changed!"
        },
        {'status': HTTPStatus.OK},
    ),
]


test_data_for_role_appoint_fail = [
    (
        '13f82a7f-49ca-4e29-8731-8fed5e37695f',
        'privileged',
        {
            "msg": "User not found"
        },
        {'status': HTTPStatus.NOT_FOUND},
    ),
    (
        'qwe',
        'privileged',
        {
            "msg": "Bad format uuid"
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY},
    ),
    (
        '15e794ed-2286-4690-b092-793f5e51f0ec',
        'privileg',
        {
            "validation_error": {
                "query_params": [
                    {
                        "ctx": {
                            "enum_values": [
                                "standard",
                                "privileged",
                                "admin",
                                "test"
                            ]
                        },
                        "loc": [
                            "label"
                        ],
                        "msg": "value is not a valid enumeration member; "
                               "permitted: 'standard', 'privileged', 'admin', 'test'",
                        "type": "type_error.enum"
                    }
                ]
            }
        },
        {'status': HTTPStatus.BAD_REQUEST},
    ),
]


test_data_for_role_take_away_successful = [
    (
        '15e794ed-2286-4690-b092-793f5e51f0ec',
        {
            "msg": "Role changed!"
        },
        {'status': HTTPStatus.OK},
    )
]


test_data_for_role_take_away_fail = [
    (
        'qwe',
        {
            "msg": "Bad format uuid"
        },
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY},
    ),
    (
        '13f82a7f-49ca-4e29-8731-8fed5e37695f',
        {
            "msg": "User not found"
        },
        {'status': HTTPStatus.NOT_FOUND},
    )
]
