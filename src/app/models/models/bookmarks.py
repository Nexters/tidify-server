from typing import List, Optional

from pydantic import BaseModel


class BookmarkCreateRequest(BaseModel):
    title: str
    url: str


class BookmarkUpdateRequest(BaseModel):
    title: Optional[str]
    url: Optional[str]


class BookmarkResponse(BaseModel):
    id: int
    user_id: int
    title: str
    url: str

    class Config:
        orm_mode = True


class BookmarkListResponse(BaseModel):
    bookmarks: List[BookmarkResponse]
    bookmarks_count: int
