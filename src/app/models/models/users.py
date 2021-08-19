from enum import Enum

from pydantic import BaseModel, Field, Extra  # noqa


class MessageOk(BaseModel):
    message: str = Field(default="OK")


class SnsType(str, Enum):
    apple: str = "apple"
    kakao: str = "kakao"
    google: str = "google"



class Token(BaseModel):
    Authorization: str = None


class CreateTokenRequest(BaseModel):
    sns_type: SnsType
    access_token: str
    refresh_token: str


class UserInput(BaseModel):
    email: str = None
    name: str = None
    profile_img: str = None


class UserToken(BaseModel):
    id: int
    email: str = None
    name: str = None
    profile_img: str = None
    sns_type: str = None

    class Config:
        orm_mode = True


class UserMe(BaseModel):
    id: int
    email: str = None
    name: str = None
    profile_img: str = None
    sns_type: str = None

    class Config:
        orm_mode = True
