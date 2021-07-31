from fastapi import APIRouter

from .v1.auth import auth_router
from .v1.bookmarks import bookmark_router
from .v1.users import user_router

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(bookmark_router, tags=["bookmarks"])
v1_router.include_router(user_router, tags=["users"])
v1_router.include_router(auth_router, tags=["auth"])
