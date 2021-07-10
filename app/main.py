from app.core.config import get_settings
from app.fastapi import get_application
from app.db import database, engine, metadata

metadata.create_all(engine)
settings = get_settings()
app = get_application(settings)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


