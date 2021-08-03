from sqlalchemy.orm import Session

from app.models.models.bookmarks import BookmarkCreateRequest, BookmarkUpdateRequest
from database.schema import Bookmarks


async def create_bookmark(session: Session, user_id, bookmark_in: BookmarkCreateRequest):
    return Bookmarks.create(session=session, auto_commit=True, user_id=user_id, **bookmark_in.dict())


async def get_bookmark_by_id(session: Session, bookmark_id: int):
    return Bookmarks.filter(session=session, id=bookmark_id).first()


async def get_bookmarks_by_user_id(session: Session, user_id: int):
    return Bookmarks.filter(session=session, user_id=user_id).all()


def update_bookmark(session: Session, user_id: int, bookmark_id: int, bookmark_in: BookmarkUpdateRequest):
    return Bookmarks.filter(session=session, id=bookmark_id).update(auto_commit=True, user_id=user_id,
                                                                    **bookmark_in.dict())
