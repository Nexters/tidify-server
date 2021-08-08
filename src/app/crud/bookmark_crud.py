from sqlalchemy.orm import Session

from app.models.models.bookmarks import BookmarkCreateRequest, BookmarkUpdateRequest
from app.services import bookmark_svc
from database.schema import Bookmarks


async def create_bookmark(session: Session, user_id, bookmark_in: BookmarkCreateRequest):
    filled_bookmark = bookmark_svc.get_bookmark_info_with_og(bookmark_in)
    return Bookmarks.create(session=session, auto_commit=True, user_id=user_id, **filled_bookmark.dict())


async def get_bookmark_by_id(session: Session, bookmark_id: int):
    return Bookmarks.filter(session=session, id=bookmark_id).first()


async def get_bookmarks_by_user_id(session: Session, user_id: int):
    return Bookmarks.filter(session=session, user_id=user_id).all()


def update_bookmark(session: Session, user_id: int, bookmark_id: int, bookmark_in: BookmarkUpdateRequest):
    return Bookmarks.filter(session=session, id=bookmark_id).update(auto_commit=True, user_id=user_id,
                                                                    **bookmark_in.dict())
