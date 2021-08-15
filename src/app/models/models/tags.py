from pydantic import Field

from app.models.base import OrmModel
from core.consts import MaxLength


class Tag(OrmModel):
    id: int
    name: str = Field(min_length=1, max_length=MaxLength.title)

class TagResponse(Tag):
    pass

