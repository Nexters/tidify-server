from enum import Enum


class Phase(str, Enum):
    test: str = "test"
    local: str = "local"
    sandbox: str = "sandbox"
    production: str = "production"


class MaxLength:
    base = 255
    email = 255
    url = 1000
    title = 50
    color = 20


JWT_SECRET = "ABCD1234!"
JWT_ALGORITHM = "HS256"
EXCEPT_PATH_LIST = ["/", "/openapi.json"]
API_VERSION_PREFIX: str = "/api/v1"
EXCEPT_PATH_REGEX = f"^(/docs|/redoc|{API_VERSION_PREFIX}/oauth)"
JWT_HEADER_NAME = "tidify-oauth"

GOOGLE_APIS = {
    'user_info': 'https://openidconnect.googleapis.com/v1/userinfo?access_token={access_token}'
}

APPLE_APIS = {
    'user_info': 'https://openidconnect.googleapis.com/v1/userinfo?access_token={access_token}'
}
