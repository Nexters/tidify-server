from pydantic import Field, BaseModel

from app.models.base import OrmModel
from core.consts import MaxLength


class Tag(OrmModel):
    id: int
    name: str = Field(min_length=1, max_length=MaxLength.title)
    # TODO: Color


class TagResponse(Tag):
    pass


class TagCreateDto(BaseModel):
    name: str = Field(min_length=1, max_length=MaxLength.title)
    # TODO: Color
