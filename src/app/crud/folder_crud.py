import psycopg2
import sqlalchemy
from sqlalchemy.orm import Session

from app.models.models.folders import FolderCreateRequest, FolderUpdateRequest
from core.errors.exceptions import FolderDuplicateException
from database.schema import Folders


async def create_folder(session: Session, user_id: int, folder_in: FolderCreateRequest):
    name = folder_in.name
    color = folder_in.color.as_hex()
    try:
        folder = Folders.create(session=session, auto_commit=True, user_id=user_id, name=name, color=color)
        return folder
    except sqlalchemy.exc.IntegrityError as err:
        if isinstance(err.orig, psycopg2.errors.UniqueViolation):
            raise FolderDuplicateException(user_id, folder.name)
        raise err


async def update_folder(session: Session, user_id: int, folder_id: int, folder_in: FolderUpdateRequest):
    folder = get_folder_by_id(session, user_id, folder_id)
    folder_update_data = folder_in.dict(exclude_unset=True)
    for key, value in folder_update_data.items():
        if key == 'color':
            value = value.as_hex()
        setattr(folder, key, value)
    session.commit()
    return folder


async def get_folder_by_id(session: Session, user_id: int, folder_id: int):
    return Folders.filter(session=session, id=folder_id, user_id=user_id).first()


async def get_folders_by_user_id(session: Session, user_id: int):
    return Folders.filter(session=session, user_id=user_id).order_by('-updated_at').all()
