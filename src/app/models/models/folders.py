from typing import Optional

from pydantic import Field
from pydantic.color import Color

from app.models.base import OrmModel
from core.consts import MaxLength


class Folder(OrmModel):
    id: int
    name: str = Field(min_length=1, max_length=MaxLength.title)
    color: str


class FolderDetailResponse(Folder):
    pass


class FolderCreateRequest(OrmModel):
    name: str = Field(min_length=1, max_length=MaxLength.title)
    color: Color


class FolderUpdateRequest(FolderCreateRequest):
    name: Optional[str] = Field(min_length=1, max_length=MaxLength.title)
    color: Optional[Color]
