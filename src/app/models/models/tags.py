from typing import Optional

from pydantic import Field

from app.models.base import OrmModel
from core.consts import MaxLength


class Tag(OrmModel):
    id: int
    name: str = Field(min_length=1, max_length=MaxLength.title)


class TagDetailResponse(Tag):
    pass


class TagCreateRequest(OrmModel):
    name: str = Field(min_length=1, max_length=MaxLength.title)


class TagUpdateRequest(TagCreateRequest):
    name: Optional[str] = Field(min_length=1, max_length=MaxLength.title)
