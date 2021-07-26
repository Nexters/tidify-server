from dataclasses import asdict
from os import environ

import uvicorn
from fastapi import FastAPI
from fastapi.security import APIKeyHeader
from pydantic import PostgresDsn
from starlette.middleware.cors import CORSMiddleware  # noqa

from app.api.v1_api import v1_router
from database.conn import db
from src.core.config import get_conf

API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)


def create_app(environment):
    _app = FastAPI(title="tidify")
    conf = get_conf(environment)
    db.init_app(_app, **asdict(conf))

    _app.add_middleware(
            CORSMiddleware,
            allow_origins=conf.ALLOW_SITE,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
    )

    _app.include_router(v1_router)
    return _app


env = environ.get("ENVIRONMENT", "local")
app = create_app(env)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
