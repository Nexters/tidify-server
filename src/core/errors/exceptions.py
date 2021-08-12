class StatusCode:
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405


class APIException(Exception):
    status_code: int
    code: str
    msg: str
    detail: str
    ex: Exception

    def __init__(
            self,
            *,
            status_code: int = StatusCode.HTTP_500,
            code: str = "000000",
            msg: str = None,
            detail: str = None,
            ex: Exception = None,
    ):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.detail = detail
        self.ex = ex
        super().__init__(ex)


class UserNotFoundException(APIException):
    def __init__(self, user_id: int = None, ex: Exception = None):
        super().__init__(
                status_code=StatusCode.HTTP_404,
                msg=f"해당 유저를 찾을 수 없습니다.",
                detail=f"Not Found User ID : {user_id}",
                code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
                ex=ex,
        )


class TokenExpiredException(APIException):
    def __init__(self, detail="Token Expired", ex: Exception = None):
        super().__init__(
                status_code=StatusCode.HTTP_400,
                msg=f"세션이 만료되어 로그아웃 되었습니다.",
                detail=detail,
                code=f"{StatusCode.HTTP_400}{'2'.zfill(4)}",
                ex=ex,
        )


class TokenDecodeException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
                status_code=StatusCode.HTTP_400,
                msg=f"비정상적인 접근입니다.",
                detail="Token has been compromised.",
                code=f"{StatusCode.HTTP_400}{'3'.zfill(4)}",
                ex=ex,
        )


class UnAuthorizedException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
                status_code=StatusCode.HTTP_401,
                msg=f"로그인이 필요한 서비스 입니다.",
                detail="Authorization Required",
                code=f"{StatusCode.HTTP_401}{'1'.zfill(4)}",
                ex=ex,
        )


class BookmarkNotFoundException(APIException):
    def __init__(self, bookmark_id: int, ex: Exception = None):
        super().__init__(
                msg=f"{bookmark_id}에 해당하는 북마크가 없습니다",
                status_code=StatusCode.HTTP_404,
                detail="Bookmark Not Found Error",
                code=f"{StatusCode.HTTP_404}{'1'.zfill(4)}",
                ex=ex,
        )


class SqlFailureException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
                status_code=StatusCode.HTTP_500,
                msg=f"이 에러는 서버측 에러 입니다. 자동으로 리포팅 되며, 빠르게 수정하겠습니다.",
                detail="Internal Server Error",
                code=f"{StatusCode.HTTP_500}{'1'.zfill(4)}",
                ex=ex,
        )
