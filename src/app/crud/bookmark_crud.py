import psycopg2
import sqlalchemy
from sqlalchemy.orm import Session, selectinload

from app.crud import tag_crud
from app.models.models.bookmarks import BookmarkCreateRequest, BookmarkUpdateRequest
from core.errors.exceptions import BookmarkUrlDuplicateException, FolderNotFoundException
from database.schema import Bookmarks, Tags, Folders


async def create_bookmark(session: Session, user_id: int, bookmark_in: BookmarkCreateRequest):
    try:
        bookmark = Bookmarks.create(session=session, auto_commit=False, user_id=user_id, **bookmark_in.dict())
    except sqlalchemy.exc.IntegrityError as err:
        if isinstance(err.orig, psycopg2.errors.UniqueViolation):
            raise BookmarkUrlDuplicateException(url=bookmark_in.url)
        if isinstance(err.orig, psycopg2.errors.ForeignKeyViolation):
            raise FolderNotFoundException(folder_id=bookmark_in.folder_id)
        raise err

    if bookmark_in.tags:
        tags = await tag_crud.get_tags_by_ids(session, user_id, bookmark_in.tags)
        bookmark.tags.extend(tags)
    session.commit()
    return bookmark


async def update_bookmark(session: Session, user_id: int, bookmark_id: int, bookmark_in: BookmarkUpdateRequest):
    bookmark = await get_bookmark_by_id(session, user_id, bookmark_id)
    bookmark.tags.clear()

    if bookmark_in.tags:
        tags = await tag_crud.get_tags_by_ids(session, user_id, bookmark_in.tags)
        bookmark.tags.extend(tags)

    bookmark_update_data = bookmark_in.dict(exclude={"tags"}, exclude_unset=True)
    for key, value in bookmark_update_data.items():
        setattr(bookmark, key, value)
    session.commit()
    return bookmark


async def get_bookmark_by_id(session: Session, user_id: int, bookmark_id: int):
    return Bookmarks.filter(session=session, id=bookmark_id, user_id=user_id).first()


async def get_bookmarks_by_user_id(session: Session, user_id: int) -> Bookmarks:
    desc_expression = sqlalchemy.sql.expression.desc(Bookmarks.updated_at)
    return session.query(Bookmarks) \
        .filter_by(user_id=user_id) \
        .order_by(desc_expression) \
        .options(selectinload(Bookmarks.tags)).all()


async def search_bookmarks_by_keyword(session: Session, user_id: int, kw: str) -> Bookmarks:
    search = f"%{kw}%"
    filter_query = (
            Bookmarks.title.ilike(search) |
            Bookmarks.url.ilike(search) |
            Tags.name.ilike(search) |
            Folders.name.ilike(search)
    )

    desc_expression = sqlalchemy.sql.expression.desc(Bookmarks.updated_at)
    return session.query(Bookmarks) \
        .filter_by(user_id=user_id) \
        .order_by(desc_expression) \
        .join(Tags, Bookmarks.tags) \
        .join(Folders, Bookmarks.folder_id == Folders.id) \
        .filter(filter_query).distinct().all()
