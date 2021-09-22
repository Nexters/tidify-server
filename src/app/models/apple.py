from pydantic.main import BaseModel


class AppleRedirectAuthCode(BaseModel):
    state: str
    code: str
