import os

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine
)
from sqlalchemy.sql import func

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
bookmarks = Table(
        "bookmarks",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("member_id", Integer),
        Column("title", String(50)),
        Column("url", String(100)),
        Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
        Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)

# databases query builder
database = Database(DATABASE_URL)
