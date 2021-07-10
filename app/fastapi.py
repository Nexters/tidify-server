from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from app.core.config import Settings

from app.api.v1_api import router as v1_router



def get_application(settings: Settings) -> FastAPI:
    _app = FastAPI(title=settings.PROJECT_NAME)

    if settings.BACKEND_CORS_ORIGINS:
        _app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
        )

    _app.include_router(v1_router)

    add_pagination(_app)

    return _app
