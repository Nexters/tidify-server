from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl

from app.models.base import OrmModel
from core.consts import MaxLength


class Bookmark(OrmModel):
    id: int
    user_id: int
    title: str = Field(min_length=1, max_length=MaxLength.title)
    url: HttpUrl
    favicon_url: Optional[str] = Field(default=None, min_length=1, max_length=MaxLength.url)
    og_url: Optional[str] = Field(default=None, min_length=1, max_length=MaxLength.url)


class BookmarkResponse(Bookmark):
    pass


class BookmarkCreateRequest(BaseModel):
    title: Optional[str] = Field(min_length=1, max_length=MaxLength.title)
    url: HttpUrl


class BookmarkWithMeta(BaseModel):
    url: HttpUrl
    title: str = Field(min_length=1, max_length=MaxLength.title)
    favicon_url: Optional[str] = Field(default=None, min_length=1, max_length=MaxLength.url)
    og_url: Optional[str] = Field(default=None, min_length=1, max_length=MaxLength.url)


class BookmarkUpdateRequest(BaseModel):
    title: Optional[str]
    url: Optional[HttpUrl]


class BookmarkListResponse(BaseModel):
    bookmarks: List[BookmarkResponse]
    bookmarks_count: int
