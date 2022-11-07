from datetime import timedelta

from models.general import RoleType
from tests.functional.utils.hash import hash_password


users_data = [

    {
        'id': '16bdbb16-d3bf-4184-b08e-e2b2eabeee7f',
        'username': 'ivan',
        'password': hash_password('ivanivanov12IN!'),
        'role': RoleType.STANDARD.name
    },
    {
        'id': '15e794ed-2286-4690-b092-793f5e51f0ec',
        'username': 'liza',
        'password': hash_password('lizaLi123!'),
        'role': RoleType.STANDARD.name
    },
    {
        'id': 'e2da75c0-8f07-4d20-bfc4-8afcf58e7a2c',
        'username': 'admin',
        'password': hash_password('adminADMINOV1!'),
        'role': RoleType.ADMIN.name
    },
    {
        'id': 'bb81ead9-b728-461b-a0a9-eacc9b7127a2',
        'username': 'oleg',
        'password': hash_password('Ldfj78!ksjd'),
        'role': RoleType.PRIVILEGED.name
    },
]

redis_users_expires_data = [
    timedelta(days=30),
    timedelta(seconds=1),
    timedelta(days=30),
]

roles_data = [

    {
        'id': '815aa676-902d-4505-bbb5-42ca9727617f',
        'label': RoleType.STANDARD
    },
    {
        'id': '13f82a7f-49ca-4e29-8731-8fed5e37695f',
        'label': RoleType.PRIVILEGED
    },
    {
        'id': 'c07d6c8c-1d4f-4f54-b88f-2c2b962ad7b6',
        'label': RoleType.ADMIN
    }
]

users_data_for_tokens = [
    {'username': 'ivan', 'role': RoleType.STANDARD.name},
    {'username': 'liza', 'role': RoleType.STANDARD.name},
    {'username': 'oleg', 'role': RoleType.PRIVILEGED.name},
    {'username': 'admin', 'role': RoleType.ADMIN.name}
]
