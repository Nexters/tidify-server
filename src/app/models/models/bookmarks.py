from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl

from app.models.base import OrmModel
from app.models.models.tags import TagResponse
from core.consts import MaxLength


class Bookmark(OrmModel):
    id: int
    url: HttpUrl
    title: Optional[str] = Field(min_length=1, max_length=MaxLength.title)
    og_img_url: Optional[str] = Field(default=None, min_length=1, max_length=MaxLength.url)
    tags: Optional[List[TagResponse]]


class BookmarkDetailResponse(Bookmark):
    pass


class BookmarkCreateRequest(BaseModel):
    url: HttpUrl
    title: Optional[str] = Field(min_length=1, max_length=MaxLength.title)
    og_img_url: Optional[str]
    tags: Optional[List[str]]  # TODO: tag 이름 -> tag ids


class BookmarkUpdateRequest(BookmarkCreateRequest):
    url: Optional[HttpUrl]


class BookmarkListResponse(BaseModel):
    bookmarks: List[BookmarkDetailResponse]
    bookmarks_count: int
