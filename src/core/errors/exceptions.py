from typing import List

from fastapi import HTTPException
from starlette import status


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


class TagNotFoundException(APIException):
    def __init__(self, tag_id: int, ex: Exception = None):
        super().__init__(
            msg=f"{tag_id}에 해당하는 해시태그가 없습니다",
            status_code=StatusCode.HTTP_404,
            detail="Tag Not Found Error",
            code=f"{StatusCode.HTTP_404}{'1'.zfill(4)}",
            ex=ex,
        )


class FolderNotFoundException(APIException):
    def __init__(self, folder_id: int, ex: Exception = None):
        super().__init__(
            msg=f"{folder_id}에 해당하는 폴더가 없습니다",
            status_code=StatusCode.HTTP_404,
            detail="Folder Not Found Error",
            code=f"{StatusCode.HTTP_404}{'1'.zfill(4)}",
            ex=ex,
        )


class BookmarkUrlDuplicateException(APIException):
    def __init__(self, url: str, ex: Exception = None):
        super().__init__(
            msg=f"{url}에 해당하는 북마크가 이미 존재합니다.",
            status_code=StatusCode.HTTP_400,
            detail="Bookmark Url Duplicate Error",
            code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
            ex=ex,
        )


class TagDuplicateException(APIException):
    def __init__(self, user_id: int, tag_name: str, ex: Exception = None):
        super().__init__(
            msg=f"사용자({user_id})는 이미 {tag_name}에 해당하는 해시태그를 가지고 있습니다.",
            status_code=StatusCode.HTTP_400,
            detail="Tag name duplicate Error",
            code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
            ex=ex,
        )


class FolderDuplicateException(APIException):
    def __init__(self, user_id: int, folder_name: str, ex: Exception = None):
        super().__init__(
            msg=f"사용자({user_id})는 이미 {folder_name}에 해당하는 폴더를 가지고 있습니다.",
            status_code=StatusCode.HTTP_400,
            detail="Folder name duplicate Error",
            code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
            ex=ex,
        )


class InvalidTagIdExistException(APIException):
    def __init__(self, tag_ids: List[int], exist_ids: List[int], ex: Exception = None):
        super().__init__(
            msg=f"입력된 {tag_ids}에는 부적절한 태그 id가 포함 되어있습니다. 현재 존재하는 태그 ids: {exist_ids}",
            status_code=StatusCode.HTTP_400,
            detail=f"Invalid Tag is given",
            code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
            ex=ex,
        )


class SqlFailureException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_500,
            msg=f"이 에러는 서버 DB측 에러 입니다. 빠르게 수정하겠습니다.",
            detail=str(ex),
            code=f"{StatusCode.HTTP_500}{'1'.zfill(4)}",
            ex=ex,
        )


class GoogleOAuthError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google OAuth Server Occured Error")


class KakaoOAuthError(HTTPException):
    def __init__(self, detail="Kakao OAuth Server Occured Error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail)
