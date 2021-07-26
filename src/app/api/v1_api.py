from fastapi import APIRouter
from .v1.bookmarks import bookmark_router

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(bookmark_router, tags=["bookmarks"])
