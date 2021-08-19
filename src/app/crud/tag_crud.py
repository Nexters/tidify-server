from typing import List

import psycopg2
import sqlalchemy
from sqlalchemy.orm import Session

from app.models.models.tags import TagCreateRequest, TagUpdateRequest
from core.errors.exceptions import TagDuplicateException, InvalidTagIdExistException
from database.schema import Tags


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


async def get_tag_by_id(session: Session, user_id: int, tag_id: int):
    return Tags.filter(session=session, id=tag_id, user_id=user_id).first()


async def get_tags_by_ids(session: Session, user_id: int, tag_ids: List[int]):
    tags = Tags.filter(session=session, id__in=tag_ids, user_id=user_id).all()
    if len(tags) != len(tag_ids):
        exist_tag_ids = [t.id for t in tags]
        raise InvalidTagIdExistException(tag_ids=tag_ids, exist_ids=exist_tag_ids)
    return tags


async def get_tags_by_user_id(session: Session, user_id: int):
    return Tags.filter(session=session, user_id=user_id).order_by('-updated_at').all()
