from typing import List

from sqlalchemy.orm import Session

from database.schema import Tags, Bookmarks


async def create_tags_by_names(session: Session, tag_names: List[str]):
    tags = [Tags(name=name) for name in tag_names]
    session.bulk_save_objects(tags)
    return tags
