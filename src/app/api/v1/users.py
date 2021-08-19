from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request  # noqa

from app.models.models.users import UserMe
from app.services.auth_svc import AUTH_HEADER
from app.services.user_svc import get_user_by_access_token
from database.conn import db

user_router = APIRouter(prefix='/user')


@user_router.get('/me', response_model=UserMe)
async def get_me(
        session: Session = Depends(db.session),
        token: str = Depends(AUTH_HEADER),
):
    return await get_user_by_access_token(token, session)


@user_router.put('/me')
async def put_me(token: str = Depends(AUTH_HEADER)):
    ...


@user_router.delete('/me')
async def delete_me(token: str = Depends(AUTH_HEADER)):
    ...
