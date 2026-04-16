import os
from typing import Any, Mapping, Optional

from flask import Flask

from . import auth, blog, db


def create_app(test_config: Optional[Mapping[str, Any]] = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object("flaskr.settings")
    app.config.from_envvar("FLASKR_SETTINGS", silent=True)
    if test_config:
        app.config.from_mapping(test_config)
    app.jinja_options["autoescape"] = True

    database_url = os.getenv("DATABASE_URL") or app.config["DATABASE_URL"]

    db.init_db(database_url)

    db_session, remove_session = db.create_db_session(database_url)
    app.config["DB_SESSION"] = db_session

    app.teardown_appcontext(remove_session)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    return app
