from functools import lru_cache
from typing import List

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "tidify"
    PHASE: str = "dev"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()
