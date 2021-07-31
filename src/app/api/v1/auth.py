from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse  # noqa

from app.models.models.users import Token, SnsType, CreateTokenRequest, UserInput
from app.services.auth import create_access_token, get_kakao_user_profile
from app.services.member import sign_up_if_not_signed
from database.conn import db

auth_router = APIRouter(prefix="/auth")


@auth_router.post("", status_code=201, response_model=Token)
async def get_token(token_request: CreateTokenRequest, session: Session = Depends(db.session)):
    if token_request.sns_type == SnsType.kakao:
        kakao_auth_info = await get_kakao_user_profile(token_request.access_token)  # 이메일이 없을 경우? 새로 만든다.
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
