from sqlalchemy.orm import Session

from app.crud import user_crud
from app.models.models.users import UserInput


async def sign_up_if_not_signed(session: Session, sns_type: str, user_input: UserInput) -> None:
    user = await user_crud.get_user_by_email(session=session, email=user_input.email)
    if not user:
        await user_crud.create_user(session, sns_type, user_input)
