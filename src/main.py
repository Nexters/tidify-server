import hashlib
import os
from dataclasses import asdict
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.base import BaseHTTPMiddleware  # noqa
from starlette.middleware.cors import CORSMiddleware  # noqa
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response  # noqa

from app.api.v1_api import v1_router
from core.config import get_conf
from core.consts import Phase
from core.middlewares.token_validator import access_control
from database.conn import db

_SECRET_KEY = hashlib.sha256(os.urandom(1024)).hexdigest()  # TODO: settings singleton


def create_app(phase, title="tidify"):
    _app = FastAPI(title=title)

    @_app.get("/")
    async def index():
        """
        index API
        """
        current_time = datetime.utcnow()
        return Response(f"Tidify Server (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})")

    conf = get_conf(phase)
    db.init_app(_app, **asdict(conf))
    _app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=conf.ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.add_middleware(SessionMiddleware, secret_key=_SECRET_KEY)

    _app.include_router(v1_router)

    add_pagination(_app)
    return _app


env = os.environ.get("ENVIRONMENT", Phase.local)
app = create_app(env)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
