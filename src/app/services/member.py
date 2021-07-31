from sqlalchemy.orm import Session

from app.models.models.users import UserInput
from database.schema import Users


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
