from typing import List

from pydantic import BaseModel


class BookmarkIn(BaseModel):
    member_id: int
    title: str
    url: str


class BookmarkOut(BaseModel):
    id: int
    member_id: str
    title: str
    url: str

    class Config:
        orm_mode = True


class BookmarkListOut(BaseModel):
    bookmarks: List[BookmarkOut]
    bookmarks_count: int
