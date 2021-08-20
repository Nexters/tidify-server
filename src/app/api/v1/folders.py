from fastapi import APIRouter, Depends, Path
from fastapi.params import Security
from fastapi_pagination import Page, paginate
from fastapi_pagination.bases import AbstractPage
from sqlalchemy.orm import Session

from app.crud import folder_crud
from app.models.models.folders import FolderDetailResponse, FolderCreateRequest, FolderUpdateRequest
from app.models.models.users import UserMe
from app.services.user_svc import get_current_user
from core.errors import exceptions
from core.utils.query_utils import to_dict
from database.conn import db
from database.schema import Folders

folder_router = APIRouter(prefix="/folders")
__valid_id = Path(..., title="The ID of hash folder to get", ge=1)


@folder_router.get("/", response_model=Page[FolderDetailResponse])
async def list_folders(
        current_user: UserMe = Security(get_current_user),
        session: Session = Depends(db.session)
) -> AbstractPage:
    # TODO: 폴더에 북마크 정보 추가해서 제공
    folders = await folder_crud.get_folders_by_user_id(session, user_id=current_user.id)
    return paginate(folders)


@folder_router.post("/", response_model=FolderDetailResponse, status_code=201)
async def create_folder(
        folder_in: FolderCreateRequest,
        current_user: UserMe = Security(get_current_user),
        session: Session = Depends(db.session)
) -> FolderDetailResponse:
    folder = await folder_crud.create_folder(session, current_user.id, folder_in)
    return FolderDetailResponse(**to_dict(folder))


@folder_router.get("/{folder_id}", response_model=FolderDetailResponse, status_code=200)
async def retrieve_folder(
        current_user: UserMe = Security(get_current_user),
        folder_id: int = __valid_id,
        session: Session = Depends(db.session)
) -> FolderDetailResponse:
    folder = await folder_crud.get_folder_by_id(session, current_user.id, folder_id)
    return FolderDetailResponse(**to_dict(folder))


@folder_router.patch("/{folder_id}", response_model=FolderDetailResponse, status_code=201)
async def update_folder(
        folder_in: FolderUpdateRequest,
        current_user: UserMe = Security(get_current_user),
        folder_id: int = __valid_id,
        session: Session = Depends(db.session)
) -> FolderDetailResponse:
    folder = await folder_crud.update_folder(session, current_user.id, folder_id, folder_in)
    return FolderDetailResponse(**to_dict(folder))


@folder_router.delete("/{folder_id}", status_code=204)
async def delete_folder(
        folder_id: int = __valid_id,
        current_user: UserMe = Security(get_current_user),
        session: Session = Depends(db.session)
) -> None:
    folder = Folders.filter(session=session, id=folder_id, user_id=current_user.id)

    if not folder.first():
        raise exceptions.FolderNotFoundException(folder_id=folder_id)
    folder.delete(auto_commit=True)  # TODO: bookmark root 이동 여부 확인
