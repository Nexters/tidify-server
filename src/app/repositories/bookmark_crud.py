from sqlalchemy.orm import Session

from app.models.models.bookmarks import BookmarkIn
from database.schema import Bookmarks


async def create_bookmark(session: Session, payload: BookmarkIn):
    return Bookmarks.create(session=session, auto_commit=True, member_id=payload.member_id, url=payload.url,
                            title=payload.title)


async def get_bookmarks_by_member_id(session: Session, member_id: int):
    return Bookmarks.filter(session=session, member_id=member_id).all()
