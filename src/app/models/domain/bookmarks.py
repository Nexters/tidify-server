from pydantic import BaseModel, Field

from src.app.models.common import DateTimeModelMixin, IDModelMixin


class Bookmark(IDModelMixin, DateTimeModelMixin, BaseModel):
    member_id: int = Field(...)
    title: str = Field(..., min_length=1, max_length=50)
    url: str = Field(..., min_length=1, max_length=100)
