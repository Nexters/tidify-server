from typing import List

from sqlalchemy.orm import Session

from database.schema import Tags


async def create_tags_by_names(session: Session, tag_names: List[str]):
    tags = [Tags(name=name) for name in tag_names]
    session.bulk_save_objects(tags, return_defaults=True)  # return_defaults: session에 기록
    return tags
