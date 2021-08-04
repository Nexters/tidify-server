import os
from asyncio import get_event_loop
from typing import Generator, List

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from database.conn import Base, db
from main import create_app


@pytest.fixture(scope="module")
def app():
    os.environ["ENVIRONMENT"] = "test"
    return create_app(phase="test", title="테스트")


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
    clear_all_table_data(
            session=sess,
            metadata=Base.metadata,
            except_tables=[]
    )
    sess.rollback()


def clear_all_table_data(session: Session, metadata, except_tables: List[str] = None):
    # session.execute("SET FOREIGN_KEY_CHECKS = 0;")
    for table in metadata.sorted_tables:
        if table.name not in except_tables:
            session.execute(table.delete())

    # session.execute("SET FOREIGN_KEY_CHECKS = 1;")
    session.commit()
