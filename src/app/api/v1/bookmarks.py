from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from starlette.requests import Request  # noqa

from app.models.models.bookmarks import BookmarkListResponse, BookmarkResponse, BookmarkCreateRequest, \
    BookmarkUpdateRequest
from app.crud import bookmark_crud
from core.errors import exceptions
from database.conn import db
from database.schema import Bookmarks

bookmark_router = APIRouter(prefix="/bookmarks")
__valid_id = Path(..., title="The ID of bookmark to get", ge=1)


@bookmark_router.get("/", response_model=BookmarkListResponse)
async def list_bookmarks_by_member(
        request: Request,
        session: Session = Depends(db.session)
) -> BookmarkListResponse:
    # TODO: pagination
    bookmarks = await bookmark_crud.get_bookmarks_by_user_id(session, user_id=request.state.user.id)
    return BookmarkListResponse(
            bookmarks=[BookmarkResponse(id=bookmark.id,
                                        user_id=bookmark.user_id,
                                        title=bookmark.title,
                                        url=bookmark.url) for bookmark in bookmarks],
            bookmarks_count=len(bookmarks)
    )


@bookmark_router.post("/", response_model=BookmarkResponse, status_code=201)
async def create_bookmark(
        request: Request,
        bookmark_in: BookmarkCreateRequest,
        session: Session = Depends(db.session)
) -> BookmarkResponse:
    user_id = request.state.user.id
    bookmark = await bookmark_crud.create_bookmark(session, user_id, bookmark_in)
    return BookmarkResponse(**bookmark.dict())


@bookmark_router.patch("/{bookmark_id}", response_model=BookmarkResponse, status_code=201)
async def update_bookmark(
        request: Request,
        bookmark_in: BookmarkUpdateRequest,
        bookmark_id: int = __valid_id,
        session: Session = Depends(db.session)
) -> BookmarkResponse:
    user_id = request.state.user.id
    bookmark = await bookmark_crud.update_bookmark(session, user_id, bookmark_id, bookmark_in)
    return BookmarkResponse(**bookmark.dict())


@bookmark_router.delete("/{bookmark_id}", status_code=204)
async def delete_bookmark(
        bookmark_id: int = __valid_id,
        session: Session = Depends(db.session)
) -> None:
    bookmark = Bookmarks.filter(session=session, id=bookmark_id)
    if not bookmark.first():
        raise exceptions.BookmarkNotFoundException(bookmark_id=bookmark_id)
    bookmark.delete(auto_commit=True)
