from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request  # noqa

from app.models.models.bookmarks import BookmarkListOut, BookmarkOut, BookmarkIn
from app.crud import bookmark_crud
from database.conn import db

bookmark_router = APIRouter(prefix="/bookmarks")


@bookmark_router.get("/{member_id}", response_model=BookmarkListOut)
async def list_bookmarks_by_member(request: Request, member_id: int, session: Session = Depends(db.session)):
    bookmarks = await bookmark_crud.get_bookmarks_by_member_id(session, member_id=member_id)
    return BookmarkListOut(
            bookmarks=[BookmarkOut(id=bookmark.id,
                                   member_id=bookmark.member_id,
                                   title=bookmark.title,
                                   url=bookmark.url) for bookmark in bookmarks],
            bookmarks_count=len(bookmarks)
    )


@bookmark_router.post("/", response_model=BookmarkOut, status_code=201)
async def create_bookmark(request: Request, payload: BookmarkIn, session: Session = Depends(db.session)):
    bookmark = await bookmark_crud.create_bookmark(session, payload)
    return BookmarkOut(id=bookmark.id,
                       member_id=payload.member_id,
                       title=payload.title,
                       url=payload.url)
