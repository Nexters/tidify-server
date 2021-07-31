import re
import time

import jwt
import sqlalchemy.exc
from jwt.exceptions import ExpiredSignatureError, DecodeError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.models.models.users import UserToken
from core import consts
from core.consts import EXCEPT_PATH_REGEX, EXCEPT_PATH_LIST
from core.errors import exceptions
from core.errors.exceptions import SqlFailureError, APIException
from core.utils.date_utils import D
from core.utils.logger import api_logger


async def access_control(request: Request, call_next):
    request.state.req_time = D.datetime()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None
    request.state.service = None

    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip
    headers = request.headers

    url = request.url.path
    if await _url_pattern_check(url, EXCEPT_PATH_REGEX) or url in EXCEPT_PATH_LIST:
        response = await call_next(request)
        if url != "/":
            await api_logger(request=request, response=response)
        return response

    # TODO: 로직 리팩토링
    try:
        if url.startswith("/api"):
            if "authorization" not in headers.keys():
                raise exceptions.NotAuthorized()
            if "Authorization" not in headers.keys():
                raise exceptions.NotAuthorized()
            token_info = await _token_decode(access_token=headers.get("Authorization"))
            request.state.user = UserToken(**token_info)
        response = await call_next(request)
        await api_logger(request=request, response=response)
    except Exception as e:
        error = await _exception_handler(e)
        error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
        response = JSONResponse(status_code=error.status_code, content=error_dict)
        await api_logger(request=request, error=error)

    return response


async def _url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False


async def _token_decode(access_token):
    """
    :param access_token:
    :return:
    """
    try:
        access_token = access_token.replace("Bearer ", "")
        payload = jwt.decode(access_token, key=consts.JWT_SECRET, algorithms=[consts.JWT_ALGORITHM])
    except ExpiredSignatureError:
        raise exceptions.TokenExpiredEx()
    except DecodeError:
        raise exceptions.TokenDecodeEx()
    return payload


async def _exception_handler(error: Exception):
    print(error)
    if isinstance(error, sqlalchemy.exc.OperationalError):
        error = SqlFailureError(ex=error)
    if not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))
    return error
