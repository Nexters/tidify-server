from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.base import OrmModel
from core.consts import MaxLength


class Bookmark(OrmModel):
    id: int
    user_id: int
    title: str = Field(min_length=1, max_length=MaxLength.title)
    url: str = Field(min_length=1, max_length=MaxLength.url)  # TODO: regex url
    favicon_url: Optional[str] = Field(default=None, min_length=1, max_length=MaxLength.url)
    og_url: Optional[str] = Field(default=None, min_length=1, max_length=MaxLength.url)


class BookmarkResponse(Bookmark):
    pass


class BookmarkCreateRequest(BaseModel):
    title: Optional[str] = Field(min_length=1, max_length=MaxLength.title)
    url: str = Field(min_length=1, max_length=MaxLength.url)  # TODO: regex url

class BookmarkWithMeta(BaseModel):
    url: str = Field(min_length=1, max_length=MaxLength.url)  # TODO: regex url
    title: str = Field(min_length=1, max_length=MaxLength.title)
    favicon_url: Optional[str] = Field(default=None, min_length=1, max_length=MaxLength.url)
    og_url: Optional[str] = Field(default=None, min_length=1, max_length=MaxLength.url)

class BookmarkUpdateRequest(BaseModel):
    title: Optional[str]
    url: Optional[str]


class BookmarkListResponse(BaseModel):
    bookmarks: List[BookmarkResponse]
    bookmarks_count: int
