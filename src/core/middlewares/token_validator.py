import re
import time
import traceback

import sqlalchemy.exc
from fastapi.logger import logger
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.services.users import get_user_by_access_token
from core.consts import EXCEPT_PATH_REGEX, EXCEPT_PATH_LIST, JWT_HEADER_NAME
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

    try:
        if url.startswith("/api"):
            access_token = _get_access_token_from_header(headers)
            logger.info(f'access_token:{access_token}')
            if not access_token:
                raise exceptions.UnAuthorizedException()
            request.state.user = await get_user_by_access_token(access_token)  # TODO: 중복이므로 처리 필요

        response = await call_next(request)
        await api_logger(request=request, response=response)
    except Exception as e:

        error = await _exception_handler(e)
        error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
        response = JSONResponse(status_code=error.status_code, content=error_dict)
        await api_logger(request=request, error=error)
    return response

def _get_access_token_from_header(headers):
    logger.info(headers)
    auth_code = headers.get(JWT_HEADER_NAME)
    if not auth_code:
        auth_code = headers.get("tidify_auth")
    return auth_code


async def _url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False


async def _exception_handler(error: Exception):
    logger.info(error)
    traceback.print_exc()
    if isinstance(error, sqlalchemy.exc.OperationalError):
        error = SqlFailureException(ex=error)
    if not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))
    return error
