import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # tidify-server/src
sys.path.append(BASE_DIR)

from logging.config import fileConfig
from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from core.consts import Phase
from database.conn import Base

colour = None
try:
    import colour  # noqa

    print("here")
    python_colour_type = colour.Color
except ImportError:
    python_colour_type = None

from database.schema import *  # noqa

ENV_DIR = os.path.dirname(BASE_DIR)

_env = os.environ.get("ENVIRONMENT", Phase.local)
if _env == Phase.local:
    load_dotenv(os.path.join(ENV_DIR, ".env.dev"))

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url():
    uri = os.getenv("DATABASE_URL")
    if uri.startswith("postgres://"):
        return uri.replace("postgres://", "postgresql+psycopg2://", 1)
    return uri


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            compare_type=True,
            dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
            configuration=configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
