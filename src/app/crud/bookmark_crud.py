import psycopg2
import sqlalchemy
from sqlalchemy.orm import Session, selectinload

from app.models.models.bookmarks import BookmarkCreateRequest, BookmarkUpdateRequest
from app.services import tag_svc
from core.errors.exceptions import BookmarkUrlDuplicateException
from database.schema import Bookmarks


async def create_bookmark(session: Session, user_id: int, bookmark_in: BookmarkCreateRequest):
    try:
        bookmark = Bookmarks.create(session=session, auto_commit=False, user_id=user_id, **bookmark_in.dict())
    except sqlalchemy.exc.IntegrityError as err:
        if isinstance(err.orig, psycopg2.errors.UniqueViolation):
            raise BookmarkUrlDuplicateException(url=bookmark_in.url)

    if bookmark_in.tags:
        exist_tags, new_tags = await tag_svc.get_tags_and_create_tags_if_not_existed(session, bookmark_in.tags)
        bookmark.tags.extend(exist_tags)
        bookmark.tags.extend(new_tags)
    session.commit()
    return bookmark


async def get_bookmark_by_id(session: Session, user_id: int, bookmark_id: int):
    return Bookmarks.filter(session=session, id=bookmark_id, user_id=user_id).first()


async def get_bookmarks_by_user_id(session: Session, user_id: int) -> Bookmarks:
    return session.query(Bookmarks).options(selectinload(Bookmarks.tags)).filter(Bookmarks.user_id == user_id).all()


def update_bookmark(session: Session, user_id: int, bookmark_id: int, bookmark_in: BookmarkUpdateRequest):
    return Bookmarks.filter(session=session, id=bookmark_id).update(auto_commit=True, user_id=user_id,
                                                                    **bookmark_in.dict())
