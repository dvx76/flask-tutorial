"""Database utilities for configuring and accessing SQLAlchemy sessions."""

from collections.abc import Callable
from pathlib import Path

from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .models import Base

LOCAL_DIRECTORY: Path = Path(__file__).parent
SQLITE_DB_FILE: str = str(LOCAL_DIRECTORY / "flaskr.sqlite")
DEFAULT_DATABASE_URL: str = f"sqlite:///{Path(__file__).parent / 'flaskr.sqlite'}"


def create_db_session(
    database_url: str | None = None,
) -> tuple[scoped_session[Session], Callable[[BaseException | None], None]]:
    """Create the scoped database session used by the application.

    Args:
        database_url: Database connection URL. When omitted, the local SQLite
            tutorial database is used.

    Returns:
        A tuple containing the scoped session registry and a callback that
        removes the active session at the end of a request.
    """
    database_url = database_url if database_url else DEFAULT_DATABASE_URL
    engine = create_engine(database_url)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    def remove_session(_exc: BaseException | None = None) -> None:
        db_session.remove()

    return (db_session, remove_session)


def init_db(database_url: str = DEFAULT_DATABASE_URL) -> None:
    """Recreate the database schema from the SQLAlchemy models.

    Args:
        database_url: Database connection URL to initialize.

    Warning:
        This function drops existing tables before recreating them. Use it only
        for local development, tests, or other disposable databases.
    """
    engine = create_engine(database_url, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_db_session() -> scoped_session[Session]:
    """Return the request-scoped database session.

    Returns:
        The SQLAlchemy scoped session stored on the current Flask app.

    Raises:
        RuntimeError: If called outside an active Flask application context.
    """
    return current_app.config["DB_SESSION"]


if __name__ == "__main__":
    init_db()
