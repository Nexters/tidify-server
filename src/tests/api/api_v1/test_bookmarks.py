import pytest
from httpx import AsyncClient
from pydantic import typing
from sqlalchemy.orm import Session
from starlette import status

from app.models.models.bookmarks import BookmarkCreateRequest
from core.consts import API_VERSION_PREFIX


@pytest.fixture
def bookmark_create_request() -> BookmarkCreateRequest:
    return BookmarkCreateRequest(
            title="네이버",
            url="https://naver.com",
            og_img_url="https://s.pstatic.net/static/www/mobile/edit/2016/0705/mobile_212852414260.png",
            tags=["검색", "search"]
    )


@pytest.mark.asyncio
async def test_create_bookmark(
        async_client: AsyncClient, session: Session,
        access_token: typing.Dict,
        bookmark_create_request: BookmarkCreateRequest
) -> None:
    response = await async_client.post(f"{API_VERSION_PREFIX}/bookmarks",
                                       headers=access_token,
                                       json=bookmark_create_request.dict())

    assert response.status_code == status.HTTP_201_CREATED
    content = response.json()

    assert content["id"] is not None
    assert content["url"] == bookmark_create_request.url
    assert content["title"] == bookmark_create_request.title
    assert content["og_img_url"] == bookmark_create_request.og_img_url

    tags = content["tags"]
    for tag in tags:
        assert tag["id"] is not None
        assert tag["name"] in bookmark_create_request.tags


@pytest.mark.asyncio
async def test_create_bookmark_without_optional_fields(
        async_client: AsyncClient,
        session: Session,
        access_token: typing.Dict,
        bookmark_create_request: BookmarkCreateRequest
) -> None:
    bookmark_create_request.title = None
    bookmark_create_request.og_img_url = None
    bookmark_create_request.tags = None
    response = await async_client.post(f"{API_VERSION_PREFIX}/bookmarks",
                                       headers=access_token,
                                       json=bookmark_create_request.dict())

    assert response.status_code == status.HTTP_201_CREATED
    content = response.json()

    assert content["id"] is not None
    assert content["title"] is None
    assert content["og_img_url"] is None
    assert content["tags"] == []


@pytest.mark.asyncio
async def test_create_bookmark_dup_fail(async_client: AsyncClient, session: Session, access_token: typing.Dict,
                                        bookmark_create_request: BookmarkCreateRequest
                                        ) -> None:
    response = await async_client.post(f"{API_VERSION_PREFIX}/bookmarks",
                                       headers=access_token,
                                       json=bookmark_create_request.dict())
    assert response.status_code == status.HTTP_201_CREATED

    dup_response = await async_client.post(f"{API_VERSION_PREFIX}/bookmarks",
                                           headers=access_token,
                                           json=bookmark_create_request.dict())

    assert dup_response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.asyncio
async def test_create_bookmark_with_invalid_url_fail(
        async_client: AsyncClient,
        access_token: typing.Dict,
        bookmark_create_request: BookmarkCreateRequest
) -> None:
    invalid_url = "ht://naver.com"
    bookmark_create_request.url = invalid_url
    response = await async_client.post(f"{API_VERSION_PREFIX}/bookmarks",
                                       headers=access_token,
                                       json=bookmark_create_request.dict())
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    invalid_url2 = "naver.com"
    bookmark_create_request.url = invalid_url2
    response = await async_client.post(f"{API_VERSION_PREFIX}/bookmarks",
                                       headers=access_token,
                                       json=bookmark_create_request.dict())
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    invalid_url3 = "http://naver"
    bookmark_create_request.url = invalid_url3
    response = await async_client.post(f"{API_VERSION_PREFIX}/bookmarks",
                                       headers=access_token,
                                       json=bookmark_create_request.dict())
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

