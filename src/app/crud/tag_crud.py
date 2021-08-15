from sqlalchemy.orm import Session

from app.models.models.tags import TagCreateDto
from database.schema import Tags


async def create_tags_by_names(session: Session, tag_names):
    tags = []
    for name in tag_names:
        tag = Tags.create(session=session, auto_commit=False, **TagCreateDto(name=name).dict())
        tags.append(tag)
    return tags
