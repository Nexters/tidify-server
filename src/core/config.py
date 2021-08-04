import os
from dataclasses import dataclass

from dotenv import load_dotenv  # noqa

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # tidify-server
_env = os.environ.get("ENVIRONMENT", "local")

if _env == 'local':
    load_dotenv(os.path.join(_BASE_DIR, ".env.dev"))


def _get_url():
    uri = os.getenv("DATABASE_URL", "postgresql+psycopg2://tidify:tidify1!@localhost:5432/tidify_db")
    if uri.startswith("postgres://"):
        return uri.replace("postgres://", "postgresql+psycopg2://", 1)
    return uri


@dataclass
class Config:
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True  # dev
    DEBUG: bool = False
    TEST_MODE: bool = False
    DATABASE_URL: str = _get_url()


@dataclass
class LocalConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True


@dataclass
class SandboxConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True


@dataclass
class ProdConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]


@dataclass
class TestConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"


_config = dict(prod=ProdConfig, sandbox=SandboxConfig, local=LocalConfig, test=TestConfig)


def get_conf(phase):
    return _config[phase]()
