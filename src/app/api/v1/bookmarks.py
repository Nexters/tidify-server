from fastapi import APIRouter

from src.app.models.dtos.bookmarks import BookmarkListOut, BookmarkOut, BookmarkIn
from src.app.repositories import bookmarks as bookmark_repo

bookmark_router = APIRouter(prefix="/bookmarks")


@bookmark_router.get("/{member_id}", response_model=BookmarkListOut)
async def list_bookmarks_by_member(member_id: int):
    bookmarks = await bookmark_repo.get_bookmarks_by_member_id(member_id=member_id)
    return BookmarkListOut(
            bookmarks=[BookmarkOut(**bookmark) for bookmark in bookmarks],
            bookmarks_count=len(bookmarks)
    )


@bookmark_router.post("/", response_model=BookmarkOut, status_code=201)
async def create_bookmark(payload: BookmarkIn):
    bookmark_id = await bookmark_repo.post(payload)

    return BookmarkOut(id=bookmark_id,
                       member_id=payload.member_id,
                       title=payload.title,
                       url=payload.url)
