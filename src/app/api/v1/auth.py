from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from starlette.responses import JSONResponse  # noqa

from app.crud import user_crud
from app.models.models.users import Token, SnsType, CreateTokenRequest, UserInput, UserToken
from app.services.auth_svc import create_access_token, get_kakao_user_profile
from app.services.user_svc import sign_up_if_not_signed
from database.conn import db

auth_router = APIRouter(prefix="/auth")


@auth_router.post("", status_code=201, response_model=Token)
async def get_token(token_request: CreateTokenRequest, session: Session = Depends(db.session)):
    if token_request.sns_type == SnsType.kakao:
        kakao_auth_info = await get_kakao_user_profile(token_request.access_token)  # 정책: 이메일이 없을 경우? 새로 만든다.
        user_input = UserInput(
                email=kakao_auth_info.kakao_account.email,
                name=kakao_auth_info.properties.nickname,
                profile_img=kakao_auth_info.properties.profile_image,
        )
        await sign_up_if_not_signed(session=session, sns_type=SnsType.kakao, user_input=user_input)
        user = await user_crud.get_user_by_email(session, user_input.email)
        user_token = UserToken.from_orm(user)
        app_token = dict(
            Authorization=f"Bearer {create_access_token(user_token)}")  # TODO: token_request.refresh_token 처리
        return app_token
    return JSONResponse(status_code=400, content=dict(msg="NOT_SUPPORTED"))
