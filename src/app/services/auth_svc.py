import httpx
import jwt
from fastapi.logger import logger
from fastapi.security import APIKeyHeader
from jwt import ExpiredSignatureError, DecodeError
from starlette.responses import RedirectResponse

from app.models.google import GoogleAuthInfo
from app.models.kakao import KakaoUserMeResponse
from app.models.users import UserToken, UserInput
from core import consts
from core.consts import JWT_SECRET, JWT_ALGORITHM, JWT_HEADER_NAME, GOOGLE_APIS
from core.errors import exceptions

AUTH_HEADER = APIKeyHeader(name=JWT_HEADER_NAME)


async def decode_token(access_token):
    """
    :param access_token:
    :return:
    """
    try:
        access_token = access_token.replace("Bearer ", "")
        payload = jwt.decode(access_token, key=consts.JWT_SECRET, algorithms=[consts.JWT_ALGORITHM])
    except ExpiredSignatureError as err:
        logger.info(err)
        raise exceptions.TokenExpiredException()
    except DecodeError as err:
        logger.info(err)
        raise exceptions.TokenDecodeException()
    return payload


def create_access_token(user_token: UserToken, expires_delta: int = None):  # TODO: exp
    to_encode = user_token.dict()
    # if expires_delta:
    #     to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_kakao_user_input(access_token: str) -> UserInput:  # noqa
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

    async with httpx.AsyncClient() as client:
        res = await client.post("https://kapi.kakao.com/v2/user/me", headers=headers)

    try:
        res.raise_for_status()
    except httpx.HTTPStatusError:
        logger.info(f'[auth kakao]:{res}')
        logger.info(f'[auth kakao json]:{res.json()}')
        raise exceptions.TokenExpiredException(detail=f"kakao login failed access_token: {access_token}")

    auth_info = KakaoUserMeResponse(**res.json())
    return UserInput(
        email=auth_info.kakao_account.email,
        name=auth_info.properties.nickname,
        profile_img=auth_info.properties.profile_image,
    )


def get_frontend_callback_response(redirect_uri, code, state):
    return RedirectResponse(
        url=f'{redirect_uri}/?code={code}&state={state}',
        status_code=302)


async def get_google_user_input(access_token: str) -> UserInput:
    url = GOOGLE_APIS['user_info'].format(access_token=access_token)
    async with httpx.AsyncClient() as client:
        res = await client.get(url)

    try:
        res.raise_for_status()
    except httpx.HTTPStatusError as err:
        logger.error(err)
        raise exceptions.TokenExpiredException(detail=f"Google login failed access_token: {access_token}")

    auth_info = GoogleAuthInfo(**res.json())
    return UserInput(
        email=auth_info.email,
        name=auth_info.name,
        profile_img=auth_info.picture,
    )


async def get_apple_user_input(access_token: str):
    logger.info(f'apple access_token {access_token}')
    pass
    # url = GOOGLE_APIS['user_info'].format(access_token=access_token)
    # async with httpx.AsyncClient() as client:
    #     res = await client.get(url)
    #
    # try:
    #     res.raise_for_status()
    # except httpx.HTTPStatusError as err:
    #     logger.error(err)
    #     raise exceptions.TokenExpiredException(detail=f"Google login failed access_token: {access_token}")
    #
    # auth_info = GoogleAuthInfo(**res.json())
    # return UserInput(
    #     email=auth_info.email,
    #     name=auth_info.name,
    #     profile_img=auth_info.picture,
    # )
