from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, Extra  # noqa

from typing import Optional

from pydantic import BaseModel, Extra


class Properties(BaseModel):
    nickname: str
    profile_image: str
    thumbnail_image: str

    class Config:
        extra = Extra.allow


class Profile(BaseModel):
    nickname: str
    thumbnail_image_url: str
    profile_image_url: str
    is_default_image: Optional[bool]

    class Config:
        extra = Extra.allow


class KakaoAccount(BaseModel):
    profile_nickname_needs_agreement: Optional[bool]
    profile_image_needs_agreement: Optional[bool]
    has_age_range: Optional[bool]
    age_range_needs_agreement: Optional[bool]
    age_range: Optional[str]
    has_gender: Optional[bool]
    gender_needs_agreement: Optional[bool]
    gender: Optional[str]
    email_needs_agreement: Optional[bool]
    has_email: Optional[bool]
    is_email_valid: Optional[bool]
    is_email_verified: Optional[bool]

    profile: Profile
    email: str

    class Config:
        extra = Extra.allow


class KakaoUserMeResponse(BaseModel):
    """ 카카오 사용자 정보 가져오기
        https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#req-user-info
    """

    id: Optional[int]
    properties: Properties
    kakao_account: KakaoAccount

    class Config:
        extra = Extra.allow
