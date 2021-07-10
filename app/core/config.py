from functools import lru_cache
from typing import List, Optional

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "tidify"
    PHASE: str = "dev"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    DATABASE_URL: Optional[str] = None
    GENERATE_SCHEMAS: bool = False

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return Settings()
