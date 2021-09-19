from pydantic.main import BaseModel


class GoogleAuthInfo(BaseModel):
    email: str = None
    name: str = None
    picture: str = None
