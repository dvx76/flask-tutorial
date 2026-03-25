"""Application factory for the Flask tutorial project."""

from collections.abc import Mapping
from typing import Any

from flask import Flask

from . import auth, blog, db


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    """Create and configure the Flask application.

    The factory loads default settings from :mod:`flaskr.settings`, applies any
    environment-specific overrides, and then wires up the database session and
    blueprints used by the tutorial app.

    Args:
        test_config: Optional configuration values that override the default
            settings. This is primarily used by tests.

    Returns:
        The configured Flask application instance.

    Examples:
        >>> app = create_app({"TESTING": True, "SECRET_KEY": "test"})
        >>> app.config["TESTING"]
        True
    """
    app = Flask(__name__)
    app.config.from_object("flaskr.settings")
    app.config.from_envvar("FLASKR_SETTINGS", silent=True)
    if test_config:
        app.config.from_mapping(test_config)
    app.jinja_options["autoescape"] = True

    db_session, remove_session = db.create_db_session(app.config["DATABASE_URL"])
    app.config["DB_SESSION"] = db_session

    app.teardown_appcontext(remove_session)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    return app
