from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request  # noqa

from app.models.models.bookmarks import BookmarkListOut, BookmarkOut, BookmarkIn
from app.repositories import bookmark_crud
from database.conn import db

bookmark_router = APIRouter(prefix="/bookmarks")


@bookmark_router.get("/{member_id}", response_model=BookmarkListOut)
async def list_bookmarks_by_member(member_id: int):
    bookmarks = await bookmark_crud.get_bookmarks_by_member_id(member_id=member_id)
    return BookmarkListOut(
            bookmarks=[BookmarkOut(**bookmark) for bookmark in bookmarks],
            bookmarks_count=len(bookmarks)
    )


@bookmark_router.post("/", response_model=BookmarkOut, status_code=201)
async def create_bookmark(request: Request, payload: BookmarkIn, session: Session = Depends(db.session)):
    bookmark_id = await bookmark_crud.create_bookmark(session, payload)
    return BookmarkOut(id=bookmark_id,
                       member_id=payload.member_id,
                       title=payload.title,
                       url=payload.url)
