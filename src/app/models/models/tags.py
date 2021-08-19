from typing import Optional

from pydantic import Field
from pydantic.color import Color

from app.models.base import OrmModel
from core.consts import MaxLength


class Tag(OrmModel):
    id: int
    name: str = Field(min_length=1, max_length=MaxLength.title)
    color: Color


class TagDetailResponse(Tag):
    pass


class TagCreateRequest(OrmModel):
    name: str = Field(min_length=1, max_length=MaxLength.title)
    color: Color


class TagUpdateRequest(TagCreateRequest):
    name: Optional[str] = Field(min_length=1, max_length=MaxLength.title)
    color: Optional[Color]
