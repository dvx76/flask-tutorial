import connexion
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from werkzeug.security import check_password_hash

from .db import create_db_session
from .models import Post, User


class ResourceNotFound(connexion.ProblemException):
    def __init__(self, resource_id: int | None = None):
        super().__init__(
            status=404,
            title="NotFound",
            detail=f"Resource {resource_id if resource_id else ''} does not exist",
        )


app = connexion.FlaskApp(__name__)
app.add_api("openapi.yaml")

db_session, remove_session = create_db_session(None)
app.app.teardown_appcontext(remove_session)


def auth(username: str, password: str):
    user = db_session.scalar(select(User).where(User.username == username))

    if user and check_password_hash(user.password, password):
        return {"sub": user.id, "username": username}
    return


def _post_to_dict(post: Post) -> dict:
    return {
        "id": post.id,
        "author": post.author.username,
        "created": post.created,
        "title": post.title,
        "body": post.body,
    }


def get_all_posts():
    posts = db_session.scalars(
        select(Post).options(joinedload(Post.author)).order_by(Post.created.desc())
    )
    return [_post_to_dict(post) for post in posts]


def create_post(body: dict, token_info: dict):
    post = Post(title=body["title"], body=body["body"], author_id=token_info["sub"])
    db_session.add(post)
    db_session.commit()
    return _post_to_dict(post)


def get_post(id: int):
    post = db_session.scalar(
        select(Post).options(joinedload(Post.author)).where(Post.id == id)
    )

    if not post:
        raise ResourceNotFound(id)

    return _post_to_dict(post)


def update_post(id: int, body: dict, token_info: dict):
    post = db_session.scalar(
        select(Post).options(joinedload(Post.author)).where(Post.id == id)
    )

    if not post or post.author_id != token_info["sub"]:
        raise ResourceNotFound(id)

    post.title = body["title"]
    post.body = body["body"]
    db_session.commit()

    return _post_to_dict(post)


def delete_post(id: int, token_info: dict):
    post = db_session.scalar(
        select(Post).options(joinedload(Post.author)).where(Post.id == id)
    )

    if not post or post.author_id != token_info["sub"]:
        raise ResourceNotFound(id)

    db_session.delete(post)
    db_session.commit()

    return None, 204


if __name__ == "__main__":
    app.run("flaskr.app:app", port=5000)
