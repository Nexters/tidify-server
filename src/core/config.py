import os
from dataclasses import dataclass

from dotenv import load_dotenv  # noqa

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # tidify-server
load_dotenv(os.path.join(_BASE_DIR, ".env"))  # TODO: phase 분리, phase별로 env 네이밍 변경


# POSTGRES_HOST = os.getenv("POSTGRES_HOST")
# POSTGRES_DB = os.getenv("POSTGRES_DB")
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


@dataclass
class Config:
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True  # dev
    DEBUG: bool = False
    TEST_MODE: bool = False
    DB_URL: str = os.getenv("DATABASE_URL")


@dataclass
class LocalConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True


@dataclass
class ProdConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]


@dataclass
class TestConfig(Config):
    DB_URL: str = "mysql+pymysql://travis@localhost/notification_test?charset=utf8mb4"  # TODO: test 로컬 환경 생성
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True


_config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)


def get_conf(env):
    return _config[env]()
