from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    func, String,
    Enum, ForeignKey, Table, UniqueConstraint, PrimaryKeyConstraint, )
from sqlalchemy.orm import Session, relationship, backref

from app.models.models.users import SnsType
from core.consts import MaxLength
from database.conn import db, Base


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())

    def __init__(self):
        self._q = None
        self._session = None
        self.served = None

    def all_columns(self):
        return [c for c in self.__table__.columns if c.primary_key is False and c.name != "created_at"]

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def create(cls, session: Session, auto_commit=False, **kwargs):
        """
        테이블 데이터 적재 전용 함수
        :param session:
        :param auto_commit: 자동 커밋 여부
        :param kwargs: 적재 할 데이터
        :return:
        """
        obj = cls()
        for col in obj.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))
        session.add(obj)
        session.flush()
        if auto_commit:
            session.commit()
        return obj

    @classmethod
    def get(cls, session: Session = None, **kwargs):
        """
        Simply get a Row
        :param session:
        :param kwargs:
        :return:
        """
        sess = next(db.session()) if not session else session
        query = sess.query(cls)
        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)

        if query.count() > 1:
            raise Exception("Only one row is supposed to be returned, but got more than one.")
        result = query.first()
        if not session:
            sess.close()
        return result

    @classmethod
    def filter(cls, session: Session = None, **kwargs):
        """
        Simply get a Row
        :param session:
        :param kwargs:
        :return:
        """
        cond = []
        for key, val in kwargs.items():
            key = key.split("__")
            if len(key) > 2:
                raise Exception("No 2 more dunders")
            col = getattr(cls, key[0])
            if len(key) == 1:
                cond.append((col == val))
            elif len(key) == 2 and key[1] == 'gt':
                cond.append((col > val))
            elif len(key) == 2 and key[1] == 'gte':
                cond.append((col >= val))
            elif len(key) == 2 and key[1] == 'lt':
                cond.append((col < val))
            elif len(key) == 2 and key[1] == 'lte':
                cond.append((col <= val))
            elif len(key) == 2 and key[1] == 'in':
                cond.append((col.in_(val)))
        obj = cls()
        if session:
            obj._session = session
            obj.served = True
        else:
            obj._session = next(db.session())
            obj.served = False
        query = obj._session.query(cls)
        query = query.filter(*cond)
        obj._q = query
        return obj

    @classmethod
    def cls_attr(cls, col_name=None):
        if col_name:
            col = getattr(cls, col_name)
            return col
        else:
            return cls

    def order_by(self, *args: str):
        for a in args:
            if a.startswith("-"):
                col_name = a[1:]
                is_asc = False
            else:
                col_name = a
                is_asc = True
            col = self.cls_attr(col_name)
            self._q = self._q.order_by(col.asc()) if is_asc else self._q.order_by(col.desc())
        return self

    def update(self, auto_commit: bool = False, **kwargs):
        qs = self._q.update(kwargs)
        ret = None

        self._session.flush()
        if qs > 0:
            ret = self._q.first()
        if auto_commit:
            self._session.commit()
        return ret

    def first(self):
        result = self._q.first()
        self.close()
        return result

    def delete(self, auto_commit: bool = False):
        self._q.delete()
        if auto_commit:
            self._session.commit()

    def all(self):
        result = self._q.all()
        self.close()
        return result

    def count(self):
        result = self._q.count()
        self.close()
        return result

    def close(self):
        if not self.served:
            self._session.close()
        else:
            self._session.flush()


bookmark_tag_table = Table('bookmark_tag', Base.metadata,
                           Column('bookmark_id', ForeignKey('bookmarks.id', ondelete='cascade')),
                           Column('tag_id', ForeignKey('tags.id', ondelete='cascade')),
                           PrimaryKeyConstraint('bookmark_id', 'tag_id')
                           )


class Bookmarks(Base, BaseMixin):
    __tablename__ = "bookmarks"
    __table_args__ = (
        UniqueConstraint('user_id', 'url', ),
    )

    url = Column("url", String(MaxLength.url), unique=True)
    title = Column("title", String(MaxLength.title), nullable=True)
    og_img_url = Column("og_img_url", String(MaxLength.url), nullable=True, comment="og 이미지 url")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    users = relationship("Users", back_populates="bookmarks")

    # https://stackoverflow.com/a/16589154
    folder_id = Column(Integer,
                       ForeignKey('folders.id', ondelete='SET NULL'),
                       nullable=True,
                       comment="북마크와 연결된 폴더, null인 경우 / 루트로 간주한다.")
    folder = relationship('Folders', backref=backref('Bookmarks'))

    tags = relationship(
            "Tags",
            secondary=bookmark_tag_table,
            backref="bookmarks")


class Folders(Base, BaseMixin):
    __tablename__ = "folders"
    __table_args__ = (UniqueConstraint('name', 'user_id', name="folder_uidx"),)

    name = Column("name", String(MaxLength.title), nullable=False)
    color = Column("color", String(MaxLength.color), nullable=False, comment="hex color")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    users = relationship("Users", back_populates="folders")


class Tags(Base, BaseMixin):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint('name', 'user_id', name="tag_uidx"),)

    name = Column("name", String(MaxLength.title), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    users = relationship("Users", back_populates="tags")


class Users(Base, BaseMixin):
    __tablename__ = "users"

    status = Column(Enum("active", "deleted", "blocked", name="status"), default="active")
    email = Column(String(length=MaxLength.email), nullable=True, unique=True)
    name = Column(String(length=MaxLength.base), nullable=True)
    profile_img = Column(String(length=MaxLength.url), nullable=True)
    sns_type = Column(Enum("apple", "kakao", "google", name="sns_type"), nullable=True, default=SnsType.kakao)

    bookmarks = relationship("Bookmarks", back_populates="users", cascade="all, delete-orphan")
    tags = relationship("Tags", back_populates="users", cascade="all, delete-orphan")
    folders = relationship("Folders", back_populates="users", cascade="all, delete-orphan")


# alembic env.py에서 table auto search가 안된다면 import 해주어야 한다.
__all__ = ['Bookmarks', 'Tags', 'Users', 'Folders']
