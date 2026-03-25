"""Authentication views and helpers for the tutorial application."""

import functools
from collections.abc import Callable
from typing import ParamSpec

import sqlalchemy.exc
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask.typing import ResponseReturnValue
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db_session
from .models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")
P = ParamSpec("P")


@bp.route("/register", methods=("GET", "POST"))
def register() -> ResponseReturnValue:
    """Register a new user account.

    On ``GET`` requests this view renders the registration form. On ``POST``
    requests it validates the submitted credentials, creates the user, and
    redirects to the login page when registration succeeds.

    Returns:
        The rendered registration page or a redirect to the login page.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error: str | None = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            db_session = get_db_session()
            user = User(username=username, password=generate_password_hash(password))
            db_session.add(user)
            try:
                db_session.commit()
            except sqlalchemy.exc.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html.j2")


@bp.route("/login", methods=("GET", "POST"))
def login() -> ResponseReturnValue:
    """Authenticate an existing user and start a session.

    Returns:
        The rendered login form or a redirect to the blog index after a
        successful login.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error: str | None = None
        db_session = get_db_session()
        user = db_session.scalars(
            select(User).where(User.username == username)
        ).one_or_none()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            assert user is not None
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("blog.index"))

        flash(error)

    return render_template("auth/login.html.j2")


@bp.before_app_request
def load_logged_in_user() -> None:
    """Load the current user from the session into ``flask.g``.

    This runs before every request so templates and view functions can access
    ``g.user`` without repeating the database lookup themselves.
    """
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        db_session = get_db_session()
        g.user = db_session.scalars(
            select(User).where(User.id == user_id)
        ).one_or_none()


def login_required(
    view: Callable[P, ResponseReturnValue],
) -> Callable[P, ResponseReturnValue]:
    """Require an authenticated user before executing a view function.

    Args:
        view: View function to protect.

    Returns:
        A wrapped view that redirects anonymous visitors to the login page.

    Examples:
        >>> @bp.route("/drafts")
        ... @login_required
        ... def drafts():
        ...     return "Only logged-in users can see this page."

    Note:
        Place ``@login_required`` below ``@bp.route(...)`` so Flask registers
        the protected view function.
    """

    @functools.wraps(view)
    def wrapped_view(*args: P.args, **kwargs: P.kwargs) -> ResponseReturnValue:
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view


@bp.route("/logout")
def logout() -> ResponseReturnValue:
    """Clear the active session and return to the home page.

    Returns:
        A redirect to the blog index.
    """
    session.clear()
    return redirect(url_for("blog.index"))
