import os

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from core.consts import Phase


class SQLAlchemy:
    def __init__(self, app: FastAPI = None, **kwargs):
        self._engine = None
        self._session = None
        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(self, app: FastAPI, **kwargs):
        """
        DB 초기화 함수
        :param app: FastAPI 인스턴스
        :param kwargs:
        :return:
        """
        environment = kwargs.get("ENVIRONMENT", Phase.local)
        database_url = kwargs.get("DATABASE_URL")
        engine_kwargs = {
            'echo': kwargs.setdefault("DB_ECHO", True),
            'pool_recycle': kwargs.setdefault("DB_POOL_RECYCLE", 900),
            'pool_pre_ping': True,
            **({'connect_args': {"check_same_thread": False}} if environment == Phase.test else {})
        }

        self._engine = create_engine(url=database_url, **engine_kwargs)
        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

        # Base.metadata.create_all(bind=self._engine)

        @app.on_event("startup")
        def startup():
            self._engine.connect()
            logging.info("DB connected.")

        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self._engine.dispose()
            logging.info("DB disconnected")

    def get_db(self):
        """
        요청마다 DB 세션 유지 함수
        :return:
        """
        if self._session is None:
            raise Exception("must be called 'init_app'")
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine


db = SQLAlchemy()
Base = declarative_base()
