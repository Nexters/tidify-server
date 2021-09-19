from typing import Optional

from pydantic import Field, BaseModel
from pydantic.color import Color

from core.consts import MaxLength


class Folder(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=MaxLength.title)
    color: str


class FolderDetailResponse(Folder):
    pass


class FolderCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=MaxLength.title)
    color: Color


class FolderUpdateRequest(FolderCreateRequest):
    name: Optional[str] = Field(min_length=1, max_length=MaxLength.title)
    color: Optional[Color]
