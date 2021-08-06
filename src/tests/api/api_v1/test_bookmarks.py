import pytest
from httpx import AsyncClient
from pydantic import typing
from sqlalchemy.orm import Session
from starlette import status

from app.models.models.bookmarks import BookmarkCreateRequest
from core.consts import API_VERSION_PREFIX


@pytest.mark.asyncio
async def test_create_bookmark(async_client: AsyncClient, session: Session, access_token: typing.Dict) -> None:
    bookmark_create_request = BookmarkCreateRequest(title="tidify_test", url="https://tidify.com")
    response = await async_client.post(f"{API_VERSION_PREFIX}/bookmarks",
                                       headers=access_token,
                                       json=bookmark_create_request.dict())

    assert response.status_code == status.HTTP_201_CREATED

    content = response.json()
    assert "id" in content
    assert "user_id" in content
    assert content["title"] == bookmark_create_request.title
    assert content["url"] == bookmark_create_request.url


