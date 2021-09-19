from typing import Optional

from pydantic import Field, BaseModel

from core.consts import MaxLength


class Tag(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=MaxLength.title)


class TagDetailResponse(Tag):
    pass


class TagCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=MaxLength.title)


class TagUpdateRequest(TagCreateRequest):
    name: Optional[str] = Field(min_length=1, max_length=MaxLength.title)
