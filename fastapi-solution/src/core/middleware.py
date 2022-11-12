from fastapi import Request

from fastapi.responses import JSONResponse
from core.mapping import mapping
from core.utils import get_role_from_auth, prepare_url
from http import HTTPStatus



class MyMiddleware:

    async def __call__(self, request: Request, call_next):
        token = request.headers.get('Authorization')
        url = await prepare_url(request.url.path)
        role = await get_role_from_auth(token)
        if url in mapping[role]:
            response = await call_next(request)
            return response
        return JSONResponse(
            content={'msg': 'You dont have permissions for this action'},
            status_code=HTTPStatus.BAD_REQUEST
        )
