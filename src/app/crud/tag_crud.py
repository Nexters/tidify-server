from typing import List

import psycopg2
import sqlalchemy
from sqlalchemy.orm import Session

from app.models.models.tags import TagCreateRequest, TagUpdateRequest
from core.errors.exceptions import TagDuplicateException
from database.schema import Tags

# TODO: 제거
async def create_tags_by_names(session: Session, tag_names: List[str]):
    tags = [Tags(name=name) for name in tag_names]
    session.bulk_save_objects(tags, return_defaults=True)  # return_defaults: session에 기록
    return tags


async def create_tag(session: Session, user_id: int, tag_in: TagCreateRequest):
    name = tag_in.name
    color = tag_in.color.as_hex()
    try:
        tag = Tags.create(session=session, auto_commit=True, user_id=user_id, name=name, color=color)
    except sqlalchemy.exc.IntegrityError as err:
        if isinstance(err.orig, psycopg2.errors.UniqueViolation):
            raise TagDuplicateException(user_id, tag_in.name)
    return tag


async def update_tag(session: Session, user_id: int, tag_id: int, tag_in: TagUpdateRequest):
    tag = get_tag_by_id(session, user_id, tag_id)
    tag_update_data = tag_in.dict(exclude_unset=True)
    for key, value in tag_update_data.items():
        if key == 'color':
            value = value.as_hex()
        setattr(tag, key, value)
    session.commit()
    return tag


def get_tag_by_id(session: Session, user_id: int, tag_id: int):
    return Tags.filter(session=session, id=tag_id, user_id=user_id).first()
