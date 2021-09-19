from sqlalchemy.orm import Session

from app.models.users import UserInput
from database.schema import Users


async def create_user(session: Session, sns_type: str, user_input: UserInput):
    return Users.create(session,
                        auto_commit=True,
                        sns_type=sns_type,
                        name=user_input.name,
                        profile_img=user_input.profile_img,
                        email=user_input.email)


async def get_user_by_email(session: Session, email: str):
    return Users.get(session=session, email=email)
