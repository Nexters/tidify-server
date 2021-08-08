import re

from app.models.models.bookmarks import BookmarkCreateRequest
from core.utils import opengraph


async def get_filled_bookmark_data(bookmark_in: BookmarkCreateRequest):
    extra_data = opengraph.get_extra_data(bookmark_in.url)
    return {**extra_data, **bookmark_in.dict()}
