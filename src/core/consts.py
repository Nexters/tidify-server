from enum import Enum

JWT_SECRET = "ABCD1234!"
JWT_ALGORITHM = "HS256"
EXCEPT_PATH_LIST = ["/", "/openapi.json"]
API_VERSION_PREFIX: str = "/api/v1"
EXCEPT_PATH_REGEX = f"^(/docs|/redoc|{API_VERSION_PREFIX}/auth)"
JWT_HEADER_NAME = "tidify-auth"

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
