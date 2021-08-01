from dataclasses import dataclass
from os import path

from pydantic import PostgresDsn

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))  # tidify-server



# POSTGRES_HOST = os.getenv("POSTGRES_HOST")
# POSTGRES_DB = os.getenv("POSTGRES_DB")
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


@dataclass
class Config:
    BASE_DIR: str = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True  # dev
    DEBUG: bool = False
    TEST_MODE: bool = False
    DB_URL: str = PostgresDsn.build(
            scheme="postgresql",
            host="localhost",
            user="tidify",
            password="tidify1!",
            path="/tidify",
    )


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
