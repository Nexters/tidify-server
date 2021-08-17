from typing import List

from sqlalchemy.orm import Session

from database.schema import Tags, Bookmarks


async def create_tags_by_names(session: Session, tag_names: List[str]):
    tags = [Tags(name=name) for name in tag_names]
    session.bulk_save_objects(tags, return_defaults=True)
    return tags


async def get_tags_by_bookmark_id(session: Session, bookmark_id: int):
    return Bookmarks.filter(session=session, id=bookmark_id).tags
