import os
from asyncio import get_event_loop
from typing import Generator, List

import pytest
from httpx import AsyncClient
from pydantic import typing
from sqlalchemy.orm import Session

from app.crud import user_crud
from app.models.users import UserInput, UserToken
from app.services.auth_svc import create_access_token
from core.consts import Phase, JWT_HEADER_NAME
from database.conn import Base, db
from main import create_app


@pytest.fixture(scope="module")
def app():
    os.environ["ENVIRONMENT"] = Phase.test
    return create_app(phase=Phase.test, title="테스트")


@pytest.fixture(scope="module")
async def async_client(app) -> Generator:
    Base.metadata.create_all(db.engine)
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="module")
def event_loop():
    loop = get_event_loop()
    yield loop


@pytest.fixture(scope="function", autouse=True)
def session():
    sess = next(db.session())
    yield sess
    _clear_all_table_data(
            session=sess,
            metadata=Base.metadata,
            except_tables=[]
    )
    sess.rollback()


@pytest.fixture(scope="function")
async def access_token(session) -> typing.Dict:
    """
    테스트전 사용자 미리 등록
    :param session:
    :return:
    """
    mock_user_input = UserInput(
            email="test@test.com",
            name="테스터",
            profile_img="https://images.unsplash.com/photo-1529665253569-6d01c0eaf7b6?ixid"
                        "=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1876&q=80",
    )

    await user_crud.create_user(session, sns_type='kakao', user_input=mock_user_input)
    user = await user_crud.get_user_by_email(session, mock_user_input.email)
    session.commit()
    user_token = UserToken.from_orm(user)
    app_token = {JWT_HEADER_NAME: f"Bearer {create_access_token(user_token)}"}
    return app_token


def _clear_all_table_data(session: Session, metadata, except_tables: List[str] = None):
    # session.execute("SET FOREIGN_KEY_CHECKS = 0;")
    for table in metadata.sorted_tables:
        if table.name not in except_tables:
            session.execute(table.delete())

    # session.execute("SET FOREIGN_KEY_CHECKS = 1;")
    session.commit()
