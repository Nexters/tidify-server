import jwt
import requests

from app.models.models.kakao import KakaoUserMeResponse
from app.models.models.users import UserInput
from core.consts import JWT_SECRET, JWT_ALGORITHM


def create_access_token(user_input: UserInput, expires_delta: int = None): # TODO: exp
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
