from typing import List

from sqlalchemy.orm import Session

from app.models.models.tags import TagCreateDto
from database.schema import Tags, Bookmarks


async def create_tags_by_names(session: Session, tag_names: List[str]):
    tags = []
    for name in tag_names:
        tag = Tags.create(session=session, auto_commit=False, **TagCreateDto(name=name).dict())
        tags.append(tag)
    return tags


async def get_tags_by_bookmark_id(session: Session, bookmark_id: int):
    return Bookmarks.filter(session=session, id=bookmark_id).tags
