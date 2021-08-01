import re
import time

import sqlalchemy.exc
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.models.models.users import UserToken
from app.services.auth import decode_token
from app.services.users import get_user_by_access_token
from core.consts import EXCEPT_PATH_REGEX, EXCEPT_PATH_LIST
from core.errors import exceptions
from core.errors.exceptions import SqlFailureException, APIException
from core.utils.date_utils import D
from core.utils.logger import api_logger


async def access_control(request: Request, call_next):
    request.state.req_time = D.datetime()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None

    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip
    headers = request.headers

    url = request.url.path
    if await _url_pattern_check(url, EXCEPT_PATH_REGEX) or url in EXCEPT_PATH_LIST:
        response = await call_next(request)
        if url != "/":
            await api_logger(request=request, response=response)
        return response

    if url.startswith("/api"):
        access_token = _get_access_token_from_header(headers)
        if not access_token:
            raise exceptions.UnAuthorizedException()
        request.state.user = await get_user_by_access_token(access_token)

    response = await call_next(request)
    await api_logger(request=request, response=response)
    return response

    # for debug
    # try:
    #     if url.startswith("/api"):
    #         access_token = _get_access_token_from_header(headers)
    #         if not access_token:
    #             raise exceptions.UnAuthorizedException()
    #         token_info = await decode_token(access_token=access_token)
    #         request.state.user = UserToken(**token_info)
    #     response = await call_next(request)
    #     await api_logger(request=request, response=response)
    # except Exception as e:
    # error = await _exception_handler(e)
    # error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
    # response = JSONResponse(status_code=error.status_code, content=error_dict)
    # await api_logger(request=request, error=error)
    # return response


def _get_access_token_from_header(headers):
    auth_code = headers.get("Authorization")
    if not auth_code:
        auth_code = headers.get("authorization")
    return auth_code


async def _url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False


async def _exception_handler(error: Exception):
    print(error)
    if isinstance(error, sqlalchemy.exc.OperationalError):
        error = SqlFailureException(ex=error)
    if not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))
    return error
