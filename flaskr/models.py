"""SQLAlchemy ORM models used by the tutorial blog application."""

from datetime import datetime

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import current_timestamp


class Base(DeclarativeBase):
    """Base class shared by all ORM models in the project."""

    pass


class User(Base):
    """Registered user account.

    Users can author blog posts and authenticate with a stored password hash.
    """

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="author")


class Post(Base):
    """Blog post written by a :class:`User`.

    Each post stores a title, body text, creation timestamp, and the author who
    wrote it.
    """

    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created: Mapped[datetime] = mapped_column(server_default=current_timestamp())
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    author: Mapped[User] = relationship(back_populates="posts")
