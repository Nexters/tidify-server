import os

from authlib.integrations.base_client import OAuthError
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends
from fastapi.logger import logger
from sqlalchemy.orm import Session
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import JSONResponse  # noqa

from app.crud import user_crud
from app.models.apple import AppleRedirectAuthCode
from app.models.users import Token, SnsType, CreateTokenRequest, UserInput, UserToken
from app.services.auth_svc import create_access_token, get_kakao_user_input, get_google_user_input, get_apple_user_input
from app.services.user_svc import sign_up_if_not_signed
from core.config import get_conf
from core.consts import Phase
from core.errors import exceptions
from database.conn import db

phase = os.environ.get("ENVIRONMENT", Phase.local)
conf = get_conf(phase)
auth_router = APIRouter(prefix="/oauth")


def create_oauth_client():
    oauth = OAuth(Config())
    oauth.register(
        name='google',
        client_id=os.environ.get('GOOGLE_CLIENT_ID'),
        client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    # https://developer.okta.com/blog/2019/06/04/what-the-heck-is-sign-in-with-apple
    oauth.register(
        name='apple',
        client_id=os.environ.get('APPLE_CLIENT_ID'),
        client_secret=os.environ.get('APPLE_CLIENT_SECRET'),
        server_metadata_url='https://appleid.apple.com/.well-known/openid-configuration',
        client_kwargs={
            'response_type': 'code',
            'response_mode': 'form_post',
            'scope': 'openid email name'
        }
    )  # apple은 profile image 없다.
    return oauth


oauth_client = create_oauth_client()


@auth_router.post("", status_code=201, response_model=Token)
async def get_token(request: Request, token_request: CreateTokenRequest, session: Session = Depends(db.session)):
    logger.info(f'get_token: {token_request.access_token}')
    user_input = None
    if token_request.sns_type == SnsType.kakao:
        user_input = await get_kakao_user_input(token_request.access_token)  # 정책: 이메일이 없을 경우? 새로 만든다.
    elif token_request.sns_type == SnsType.google:
        user_input = await get_google_user_input(token_request.access_token)
    elif token_request.sns_type == SnsType.apple:
        user_input = await get_apple_user_input(token_request.access_token)
    else:
        return JSONResponse(status_code=400, content=dict(msg="NOT_SUPPORTED"))

    await sign_up_if_not_signed(session=session, sns_type=token_request.sns_type, user_input=user_input)
    user = await user_crud.get_user_by_email(session, user_input.email)
    user_token = UserToken.from_orm(user)

    # TODO: token_request.refresh_token 처리
    app_token = dict(Authorization=f"Bearer {create_access_token(user_token)}")
    return app_token


@auth_router.get('/google')
async def login(request: Request):
    redirect_uri = request.url_for('redirect_google')
    return await oauth_client.google.authorize_redirect(request=request, redirect_uri=redirect_uri)


@auth_router.get("/redirect_google")
async def redirect_google(request: Request):
    try:
        token = await oauth_client.google.authorize_access_token(request)
        logger.info(token)
    except OAuthError as error:
        logger.error(error)
        raise exceptions.GoogleOAuthError()
    return token


@auth_router.get('/apple')
async def login(request: Request):
    http_redirect_uri = request.url_for('redirect_apple')
    https_redirect_uri = http_redirect_uri.replace('http', 'https', 1)
    return await oauth_client.apple.authorize_redirect(request=request, redirect_uri=https_redirect_uri)



@auth_router.post("/redirect_apple")
async def redirect_apple(request: Request):
    try:
        logger.info(await request.json())
        token = await oauth_client.apple.authorize_access_token(request)
        logger.info(token)
    except OAuthError as error:
        logger.error(error)
        raise exceptions.AppleOAuthError()
    return token
