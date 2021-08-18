from typing import List

from fastapi.logger import logger
from sqlalchemy.orm import Session

from app.crud import tag_crud
from database.schema import Tags


async def get_tags_and_create_tags_if_not_exist(session: Session, tag_names) -> List[Tags]:
    exist_tags = Tags.filter(session=session, name__in=tag_names).all()
    logger.info(f'exist_tags: {exist_tags}')

    all_tag_name_set = set(tag_names)
    exist_tag_name_set = set([tag.name for tag in exist_tags])
    not_exist_tag_names = list(all_tag_name_set - exist_tag_name_set)

    new_tags = await tag_crud.create_tags_by_names(session, not_exist_tag_names)
    logger.info(f'new_tags: {new_tags}')

    return exist_tags + new_tags
