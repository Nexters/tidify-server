from fastapi import APIRouter
from .v1.bookmarks import bookmark_router

router = APIRouter(prefix="/api/v1")

router.include_router(bookmark_router, tags=["bookmarks"])
