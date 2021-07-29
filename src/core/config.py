from dataclasses import dataclass

from os import path, environ

from pydantic import PostgresDsn

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))  # tidify-server


# POSTGRES_HOST = os.getenv("POSTGRES_HOST", 'ec2-52-5-1-20.compute-1.amazonaws.com')
# POSTGRES_NAME = os.getenv("POSTGRES_NAME", 'ddq5ksej7gtep6')
# POSTGRES_USER = os.getenv("POSTGRES_USER", 'dcvudhthivliek')
# POSTGRES_PORT = os.getenv("POSTGRES_PORT", '5432')
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD",
#                               '94b792441ea21663cbe53a3c592971b3d67b4a7dd91e8764fc21726021682dc6')
# DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"


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
            path="/tidify_dev",
    )
    DB_URL: str = environ.get("DB_URL", "mysql+pymysql://tidify:tidify1!@127.0.0.1/tidify?charset=utf8mb4")


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
    DB_URL: str = "mysql+pymysql://travis@localhost/notification_test?charset=utf8mb4"
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True


_config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)


def get_conf(env):
    return _config[env]()
