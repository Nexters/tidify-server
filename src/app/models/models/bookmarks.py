from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl

from app.models.base import OrmModel
from app.models.models.folders import FolderDetailResponse
from app.models.models.tags import TagDetailResponse
from core.consts import MaxLength


class Bookmark(OrmModel):
    id: int
    url: HttpUrl
    title: Optional[str] = Field(min_length=1, max_length=MaxLength.title)
    og_img_url: Optional[str] = Field(default=None, min_length=1, max_length=MaxLength.url)
    folder: Optional[FolderDetailResponse]
    tags: Optional[List[TagDetailResponse]]


class BookmarkDetailResponse(Bookmark):
    pass


class BookmarkCreateRequest(BaseModel):
    url: HttpUrl
    title: Optional[str] = Field(min_length=1, max_length=MaxLength.title)
    og_img_url: Optional[str]
    folder_id: Optional[int]
    tags: Optional[List[int]]


class BookmarkUpdateRequest(BookmarkCreateRequest):
    url: Optional[HttpUrl]


class BookmarkListResponse(BaseModel):
    bookmarks: List[BookmarkDetailResponse]
    bookmarks_count: int
