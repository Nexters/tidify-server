from sqlalchemy.orm import Session

from app.models.models.bookmarks import BookmarkCreateRequest, BookmarkUpdateRequest
from app.services import tag_svc
from database.schema import Bookmarks
from fastapi.logger import logger


async def create_bookmark(session: Session, user_id, bookmark_in: BookmarkCreateRequest):
    # auto commit = False
    bookmark = Bookmarks.create(session=session, auto_commit=False, user_id=user_id, **bookmark_in.dict())
    if bookmark_in.tags:
        tags = await tag_svc.get_tags_and_create_tags_if_not_existed(session, bookmark_in.tags)
        logger.info(tags)
        bookmark.tags.extend(tags)
    session.commit()
    return bookmark


async def get_bookmark_by_id(session: Session, bookmark_id: int):
    return Bookmarks.filter(session=session, id=bookmark_id).first()


async def get_bookmarks_by_user_id(session: Session, user_id: int):
    return Bookmarks.filter(session=session, user_id=user_id).all()


def update_bookmark(session: Session, user_id: int, bookmark_id: int, bookmark_in: BookmarkUpdateRequest):
    return Bookmarks.filter(session=session, id=bookmark_id).update(auto_commit=True, user_id=user_id,
                                                                    **bookmark_in.dict())
