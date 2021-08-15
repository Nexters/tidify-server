from sqlalchemy.orm import Session

from app.crud import tag_crud
from database.schema import Tags


async def get_tags_and_create_tags_if_not_existed(session: Session, bookmark_id, tag_names):
    exist_tags = Tags.filter(session=session, name__in=tag_names).all()
    # TODO: exist_tags에 bookmark id append

    all_tag_name_set = set(tag_names)
    exist_tag_name_set = set([tag.name for tag in exist_tags])
    not_exist_tag_names = list(all_tag_name_set - exist_tag_name_set)

    new_tags = tag_crud.create_tags_by_titles(session, bookmark_id, not_exist_tag_names)
    return exist_tags + new_tags
