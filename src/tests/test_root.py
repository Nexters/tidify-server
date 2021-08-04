import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from starlette import status


@pytest.mark.asyncio
async def test_root(async_client: AsyncClient, session: Session) -> None:
    """
    root 테스트
    :param async_client:
    :param session:
    :return:
    """
    response = await async_client.get("/")
    assert response.status_code == status.HTTP_200_OK
