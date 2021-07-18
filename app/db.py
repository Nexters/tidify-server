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

DATABASE_HOST = os.getenv("DATABASE_HOST", 'ec2-52-5-1-20.compute-1.amazonaws.com')
DATABASE_NAME = os.getenv("DATABASE_NAME", 'ddq5ksej7gtep6')
DATABASE_URER = os.getenv("DATABASE_URER", 'dcvudhthivliek')
DATABASE_PORT = os.getenv("DATABASE_PORT", 'Port')
DATABASE_PWD = os.getenv("DATABASE_PWD", '94b792441ea21663cbe53a3c592971b3d67b4a7dd91e8764fc21726021682dc6')

DATABASE_URL = os.getenv("DATABASE_URL",
                         f"postgres://{DATABASE_URER}:{DATABASE_PWD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}")

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
