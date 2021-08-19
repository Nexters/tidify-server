from fastapi import APIRouter, Depends, Path
from fastapi.params import Security
from fastapi_pagination import Page, paginate
from fastapi_pagination.bases import AbstractPage
from sqlalchemy.orm import Session

from app.crud import tag_crud
from app.models.models.tags import TagCreateRequest, TagDetailResponse, TagUpdateRequest
from app.models.models.users import UserMe
from app.services.user_svc import get_current_user
from core.errors import exceptions
from core.utils.query_utils import to_dict
from database.conn import db
from database.schema import Tags

tag_router = APIRouter(prefix="/tags")
__valid_id = Path(..., title="The ID of hash tag to get", ge=1)


@tag_router.get("/", response_model=Page[TagDetailResponse])
async def list_tags(
        current_user: UserMe = Security(get_current_user),
        session: Session = Depends(db.session)
) -> AbstractPage:
    tags = await tag_crud.get_tags_by_user_id(session, user_id=current_user.id)
    return paginate(tags)


@tag_router.post("/", response_model=TagDetailResponse, status_code=201)
async def create_tag(
        tag_in: TagCreateRequest,
        current_user: UserMe = Security(get_current_user),
        session: Session = Depends(db.session)
) -> TagDetailResponse:
    tag = await tag_crud.create_tag(session, current_user.id, tag_in)
    return TagDetailResponse(**to_dict(tag))


@tag_router.get("/{tag_id}", response_model=TagDetailResponse, status_code=200)
async def retrieve_tag(
        current_user: UserMe = Security(get_current_user),
        tag_id: int = __valid_id,
        session: Session = Depends(db.session)
) -> TagDetailResponse:
    tag = await tag_crud.get_tag_by_id(session, current_user.id, tag_id)
    return TagDetailResponse(**to_dict(tag))


@tag_router.patch("/{tag_id}", response_model=TagDetailResponse, status_code=201)
async def update_tag(
        tag_in: TagUpdateRequest,
        current_user: UserMe = Security(get_current_user),
        tag_id: int = __valid_id,
        session: Session = Depends(db.session)
) -> TagDetailResponse:
    tag = await tag_crud.update_tag(session, current_user.id, tag_id, tag_in)
    return TagDetailResponse(**to_dict(tag))


@tag_router.delete("/{tag_id}", status_code=204)
async def delete_tag(
        tag_id: int = __valid_id,
        current_user: UserMe = Security(get_current_user),
        session: Session = Depends(db.session)
) -> None:
    tag = Tags.filter(session=session, id=tag_id, user_id=current_user.id)

    if not tag.first():
        raise exceptions.TagNotFoundException(tag_id=tag_id)
    tag.delete(auto_commit=True)
