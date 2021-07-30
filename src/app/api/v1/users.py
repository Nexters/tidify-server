from fastapi import APIRouter
from starlette.requests import Request  # noqa

from app.models.models.users import UserMe
from database.schema import Users

user_router = APIRouter(prefix='/user')


@user_router.get('/me', response_model=UserMe)
async def get_me(request: Request):
    user = request.state.user
    user_info = Users.get(id=user.id)
    return user_info


@user_router.put('/me')
async def put_me(request: Request):
    ...


@user_router.delete('/me')
async def delete_me(request: Request):
    ...
