from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud import user_crud
from app.models.models.users import UserInput, UserToken, UserMe
from app.services.auth_svc import decode_token, AUTH_HEADER
from core.errors.exceptions import UserNotFoundException
from core.utils.query_utils import to_dict
from database.conn import db
from database.schema import Users


async def sign_up_if_not_signed(session: Session, sns_type: str, user_input: UserInput) -> None:
    user = await user_crud.get_user_by_email(session=session, email=user_input.email)
    if not user:
        await user_crud.create_user(session, sns_type, user_input)


async def get_user_by_access_token(access_token: str, session: Session = None) -> Users:
    token_info = await decode_token(access_token)
    user_token = UserToken(**token_info)
    return Users.get(session=session, id=user_token.id)


async def get_current_user(
        session: Session = Depends(db.session),
        token: str = Depends(AUTH_HEADER),
) -> UserMe:
    user = await get_user_by_access_token(token, session)

    if not user or user.status != 'active':
        raise UserNotFoundException(user_id=user.id)
    return UserMe(**to_dict(user))
