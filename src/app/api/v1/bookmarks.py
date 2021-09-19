from typing import Optional

from fastapi import APIRouter, Depends, Path
from fastapi.params import Security
from fastapi_pagination import Page, paginate
from fastapi_pagination.bases import AbstractPage
from sqlalchemy.orm import Session
from starlette.requests import Request  # noqa

from app.crud import bookmark_crud
from app.models.bookmarks import BookmarkDetailResponse, BookmarkCreateRequest, \
    BookmarkUpdateRequest
from app.models.users import UserMe
from app.services.user_svc import get_current_user
from core.errors import exceptions
from core.utils.query_utils import to_dict
from database.conn import db
from database.schema import Bookmarks

bookmark_router = APIRouter(prefix="/bookmarks")
__valid_id = Path(..., title="The ID of bookmarks to get", ge=1)


@bookmark_router.get("/", response_model=Page[BookmarkDetailResponse])
async def list_bookmarks_by_member(
        current_user: UserMe = Security(get_current_user),
        keyword: Optional[str] = None,
        session: Session = Depends(db.session)
) -> AbstractPage:
    if keyword:
        bookmarks = await bookmark_crud.search_bookmarks_by_keyword(session, current_user.id, keyword)
    else:
        bookmarks = await bookmark_crud.get_bookmarks_by_user_id(session, user_id=current_user.id)
    return paginate(bookmarks)


@bookmark_router.post("/", response_model=BookmarkDetailResponse, status_code=201)
async def create_bookmark(
        bookmark_in: BookmarkCreateRequest,
        current_user: UserMe = Security(get_current_user),
        session: Session = Depends(db.session)
) -> BookmarkDetailResponse:
    bookmark = await bookmark_crud.create_bookmark(session, current_user.id, bookmark_in)
    return BookmarkDetailResponse(folder=bookmark.folder, tags=bookmark.tags, **to_dict(bookmark))


@bookmark_router.get("/{bookmark_id}", response_model=BookmarkDetailResponse, status_code=200)
async def retrieve_bookmark(
        current_user: UserMe = Security(get_current_user),
        bookmark_id: int = __valid_id,
        session: Session = Depends(db.session)
) -> BookmarkDetailResponse:
    bookmark = await bookmark_crud.get_bookmark_by_id(session, current_user.id, bookmark_id)
    return BookmarkDetailResponse(folder=bookmark.folder, tags=bookmark.tags, **to_dict(bookmark))


@bookmark_router.patch("/{bookmark_id}", response_model=BookmarkDetailResponse, status_code=201)
async def update_bookmark(
        bookmark_in: BookmarkUpdateRequest,
        current_user: UserMe = Security(get_current_user),
        bookmark_id: int = __valid_id,
        session: Session = Depends(db.session)
) -> BookmarkDetailResponse:
    bookmark = await bookmark_crud.update_bookmark(session, current_user.id, bookmark_id, bookmark_in)
    return BookmarkDetailResponse(folder=bookmark.folder, tags=bookmark.tags, **to_dict(bookmark))


@bookmark_router.delete("/{bookmark_id}", status_code=204)
async def delete_bookmark(
        bookmark_id: int = __valid_id,
        current_user: UserMe = Security(get_current_user),
        session: Session = Depends(db.session)
) -> None:
    bookmark = Bookmarks.filter(session=session, id=bookmark_id, user_id=current_user.id)

    if not bookmark.first():
        raise exceptions.BookmarkNotFoundException(bookmark_id=bookmark_id)
    bookmark.delete(auto_commit=True)
