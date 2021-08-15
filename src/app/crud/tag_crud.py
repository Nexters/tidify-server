from sqlalchemy.orm import Session

from database.schema import Tags


async def create_tags_by_titles(session: Session, bookmark_id, tag_names):
    # TODO: bookmark_id 언제 줘야함?
    return session.bulk_insert_mappings(Tags, [dict(bookmark_id=bookmark_id, name=name) for name in tag_names])
