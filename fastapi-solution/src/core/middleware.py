from fastapi import Request
import requests
from fastapi.responses import JSONResponse
from api.v1 import films, genres, persons
import uuid

def get_mapping(id_film: str = 'b06ee87b-612a-49f6-92e5-f7572f383f24'):
    return {
        'ANONYMOUS': [
            films.router.url_path_for('films_scope')
        ],
        'STANDARD': [
            films.router.url_path_for('films_scope'),
            films.router.url_path_for('film_search'),
            films.router.url_path_for('film_details', film_id=id_film),
        ]
    }

exists_prefix = [films.router.prefix, genres.router.prefix, persons.router.prefix]

class MyMiddleware:
    def __init__(
            self,
            some_attribute: str,
    ):
        self.some_attribute = some_attribute

    async def __call__(self, request: Request, call_next):
        token = request.headers.get('Authorization')
        url =  request.url.path
        print(url)
        url_array = url.split('/')
        prefix = f"/{'/'.join(url_array[1:4])}"
        try:
            last = uuid.UUID(str(url_array[-1]))
        except ValueError:
            last = None
        try:
            response = requests.get('http://127.0.0.1:4555/auth/v1/users/protected', headers={"Authorization": token})
            response_body = response.json()
            if response.status_code == 200:
                role = response_body['msg']
            else:
                raise Exception
        except:
            role = 'ANONYMOUS'
        mapping = get_mapping(last)
        if url in mapping[role]:
            response = await call_next(request)
            return response
        else:
            return JSONResponse(content='You dont have permissions for this action')

