from datetime import datetime

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import current_timestamp


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    posts = relationship("Post", back_populates="author")


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created: Mapped[datetime] = mapped_column(server_default=current_timestamp())
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    author = relationship("User", back_populates="posts")
