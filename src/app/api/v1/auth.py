from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
import requests

from app.models.models.kakao import KakaoUserMeResponse
from app.models.models.users import Token, SnsType, CreateTokenRequest, UserMe, UserInput
from core.consts import JWT_SECRET, JWT_ALGORITHM
from database.conn import db
from database.schema import Users

auth_router = APIRouter(prefix="/auth")


@auth_router.post("", status_code=201, response_model=Token)
async def get_token(token_request: CreateTokenRequest, session: Session = Depends(db.session)):
    if token_request.sns_type == SnsType.kakao:
        kakao_auth_info = await get_kakao_user_profile(token_request.access_token)
        print(kakao_auth_info)
        user_input = UserInput(
                email=kakao_auth_info.kakao_account.email,
                name=kakao_auth_info.properties.nickname,
                profile_img=kakao_auth_info.properties.profile_image,
        )
        await sign_up_if_not_signed(session=session, sns_type=SnsType.kakao, user_input=user_input)
        app_token = dict(
                Authorization=f"Bearer {create_access_token(user_input)}")  # TODO: token_request.refresh_token 처리
        return app_token
    return JSONResponse(status_code=400, content=dict(msg="NOT_SUPPORTED"))


async def sign_up_if_not_signed(session: Session, sns_type: str, user_input: UserInput) -> None:
    if not is_email_exist(session=session, email=user_input.email):
        Users.create(session,
                     auto_commit=True,
                     sns_type=sns_type,
                     name=user_input.name,
                     profile_img=user_input.profile_img,
                     email=user_input.email)


async def is_email_exist(session: Session, email: str):
    get_email = Users.get(session=session, email=email)
    if get_email:
        return True
    return False


def create_access_token(user_input: UserInput, expires_delta: int = None):
    to_encode = user_input.dict()
    # if expires_delta:
    #     to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_kakao_user_profile(access_token: str) -> KakaoUserMeResponse:
    """
        GET/POST /v2/user/me HTTP/1.1
        Host: kapi.kakao.com
        Authorization: Bearer {ACCESS_TOKEN}
        Content-type: application/x-www-form-urlencoded;charset=utf-8

        {
          "id": 1604053944,
          "connected_at": "2021-07-30T10:31:47Z",
          "properties": {
            "nickname": "leoo.j",
            "profile_image": "http://k.kakaocdn.net/dn/hEQ0K/btrasVaVjWG/eKxsxDtmyye3gAAdKUaPA1/img_640x640.jpg",
            "thumbnail_image": "http://k.kakaocdn.net/dn/hEQ0K/btrasVaVjWG/eKxsxDtmyye3gAAdKUaPA1/img_110x110.jpg"
          },
          "kakao_account": {
            "profile_needs_agreement": false,
            "profile": {
              "nickname": "leoo.j",
              "thumbnail_image_url": "http://k.kakaocdn.net/dn/hEQ0K/btrasVaVjWG/eKxsxDtmyye3gAAdKUaPA1/img_110x110
              .jpg",
              "profile_image_url": "http://k.kakaocdn.net/dn/hEQ0K/btrasVaVjWG/eKxsxDtmyye3gAAdKUaPA1/img_640x640.jpg",
              "is_default_image": false
            },
            "has_email": true,
            "email_needs_agreement": false,
            "is_email_valid": true,
            "is_email_verified": true,
            "email": "minkj1992@gmail.com",
            "has_age_range": true,
            "age_range_needs_agreement": true,
            "has_birthday": true,
            "birthday_needs_agreement": true,
            "has_gender": true,
            "gender_needs_agreement": true
          }
        }
    """
    headers = {
        "authorization": f"Bearer {access_token}",
        "content-type": (
            "application/x-www-form-urlencoded;charset=utf-8"
        ),
    }

    res = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers)
    try:
        res.raise_for_status()
    except Exception as e:
        print(e)
        # logger.warning(e)
        # raise ex.KakaoMeEx
    print(res.json())
    return KakaoUserMeResponse(**res.json())
