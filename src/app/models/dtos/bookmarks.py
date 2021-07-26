from typing import List

from pydantic import BaseModel

from src.app.models.domain.bookmarks import Bookmark


class BookmarkIn(BaseModel):
    member_id: int
    title: str
    url: str


class BookmarkOut(Bookmark):
    pass


class BookmarkListOut(BaseModel):
    bookmarks: List[BookmarkOut]
    bookmarks_count: int
