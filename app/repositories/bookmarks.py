from app.db import bookmarks, database
from app.models.dtos.bookmarks import BookmarkIn


async def post(payload: BookmarkIn):
    query = bookmarks.insert().values(member_id=payload.member_id, url=payload.url, title=payload.title)
    return await database.execute(query=query)


async def get_bookmarks_by_member_id(member_id: int):
    query = bookmarks.select().where(member_id == bookmarks.c.member_id)
    return await database.fetch_all(query=query)
