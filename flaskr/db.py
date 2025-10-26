import sys
from pathlib import Path
from typing import Callable, Optional

from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .models import Base

LOCAL_DIRECTORY = Path(__file__).parent
SQLITE_DB_FILE = str(LOCAL_DIRECTORY / "flaskr.sqlite")
DEFAULT_DATABASE_URL = f"sqlite:///{Path(__file__).parent / 'flaskr.sqlite'}"


def create_db_session(
    database_url: Optional[str],
) -> tuple[scoped_session[Session], Callable]:
    database_url = database_url if database_url else DEFAULT_DATABASE_URL
    engine = create_engine(database_url)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    def remove_session(_exc=None):
        db_session.remove()

    return (db_session, remove_session)


def init_db(database_url: str):
    engine = create_engine(database_url, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_db_session() -> scoped_session[Session]:
    return current_app.config["DB_SESSION"]


if __name__ == "__main__":
    init_db(sys.argv[1])
