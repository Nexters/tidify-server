from fastapi import APIRouter, Depends, Path
from fastapi.params import Security
from sqlalchemy.orm import Session
from starlette.requests import Request  # noqa

from app.models.models.bookmarks import BookmarkListResponse, BookmarkResponse, BookmarkCreateRequest, \
    BookmarkUpdateRequest
from app.crud import bookmark_crud
from app.models.models.users import UserMe
from app.services.user_svc import get_current_user

from core.errors import exceptions
from core.utils.query_utils import to_dict
from database.conn import db
from database.schema import Bookmarks

bookmark_router = APIRouter(prefix="/bookmarks")
__valid_id = Path(..., title="The ID of bookmark to get", ge=1)


@bookmark_router.get("/", response_model=BookmarkListResponse)
async def list_bookmarks_by_member(
        current_user: UserMe = Security(get_current_user),
        session: Session = Depends(db.session)
) -> BookmarkListResponse:
    # TODO: pagination
    bookmarks = await bookmark_crud.get_bookmarks_by_user_id(session, user_id=current_user.id)
    return BookmarkListResponse(
            bookmarks=[BookmarkResponse(id=bookmark.id,
                                        user_id=bookmark.user_id,
                                        title=bookmark.title,
                                        url=bookmark.url) for bookmark in bookmarks],
            bookmarks_count=len(bookmarks)
    )


@bookmark_router.post("/", response_model=BookmarkResponse, status_code=201)
async def create_bookmark(
        bookmark_in: BookmarkCreateRequest,
        current_user: UserMe = Security(get_current_user),
        session: Session = Depends(db.session)
) -> BookmarkResponse:
    bookmark = await bookmark_crud.create_bookmark(session, current_user.id, bookmark_in)
    return BookmarkResponse(**to_dict(bookmark))


@bookmark_router.patch("/{bookmark_id}", response_model=BookmarkResponse, status_code=201)
async def update_bookmark(
        bookmark_in: BookmarkUpdateRequest,
        current_user: UserMe = Security(get_current_user),
        bookmark_id: int = __valid_id,
        session: Session = Depends(db.session)
) -> BookmarkResponse:
    bookmark = bookmark_crud.update_bookmark(session, current_user.id, bookmark_id, bookmark_in)
    return BookmarkResponse(**to_dict(bookmark))


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
