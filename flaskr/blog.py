"""Blog views for listing, creating, and editing posts."""

from flask.typing import ResponseReturnValue
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db_session
from .models import Post

bp = Blueprint("blog", __name__)


@bp.route("/")
def index() -> ResponseReturnValue:
    """Show the blog home page with the newest posts first.

    Returns:
        The rendered index page.
    """
    db_session = get_db_session()
    posts = db_session.scalars(
        select(Post).options(selectinload(Post.author)).order_by(Post.created.desc())
    )
    return render_template("blog/index.html.j2", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create() -> ResponseReturnValue:
    """Create a new post for the logged-in user.

    Returns:
        The rendered creation form or a redirect to the index page after the
        post is saved.
    """
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error: str | None = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            assert g.user is not None
            db_session = get_db_session()
            post = Post(title=title, body=body, author=g.user)
            db_session.add(post)
            db_session.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html.j2")


def get_post(id: int) -> Post:
    """Return a post and ensure the current user is allowed to edit it.

    Args:
        id: Identifier of the post to retrieve.

    Returns:
        The requested post.

    Raises:
        werkzeug.exceptions.NotFound: If no post exists with the given id.
        werkzeug.exceptions.Forbidden: If the current user is not the author of
            the post.
    """
    post = get_db_session().get(Post, id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    assert g.user is not None
    if post.author_id != g.user.id:
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id: int) -> ResponseReturnValue:
    """Edit an existing post owned by the current user.

    Args:
        id: Identifier of the post to update.

    Returns:
        The rendered update form or a redirect to the index page after saving.
    """
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error: str | None = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            get_db_session().commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html.j2", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id: int) -> ResponseReturnValue:
    """Delete a post owned by the current user.

    Args:
        id: Identifier of the post to delete.

    Returns:
        A redirect to the blog index.
    """
    post = get_post(id)
    db_session = get_db_session()
    db_session.delete(post)
    db_session.commit()
    return redirect(url_for("blog.index"))
