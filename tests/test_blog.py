import pytest
from flask.testing import FlaskClient
from sqlalchemy import select

from flaskr import db, models


def test_index(client: FlaskClient):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data
    assert b"test title" in response.data
    assert b"by test on 2025-01-01" in response.data
    assert b"test\nbody" in response.data


@pytest.mark.parametrize("path", ("/create", "/1/update", "/1/delete"))
def test_login_required(client: FlaskClient, path: str):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_author_required(client: FlaskClient):
    client.post("/auth/login", data={"username": "other", "password": "other"})

    # current user can't modify other user's post
    assert client.post("/1/update").status_code == 403
    assert client.post("/1/delete").status_code == 403

    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get("/").data


@pytest.mark.parametrize(
    "path",
    (
        "/2/update",
        "/2/delete",
    ),
)
def test_post_not_exists(client: FlaskClient, path):
    client.post("/auth/login", data={"username": "test", "password": "test"})
    assert client.post(path).status_code == 404


def test_create(client: FlaskClient):
    client.post("/auth/login", data={"username": "test", "password": "test"})

    assert client.get("/create").status_code == 200
    client.post(
        "/create", data={"title": "test_create title", "body": "test_create body"}
    )

    query = select(models.Post).where(models.Post.title == "test_create title")
    post = db.get_db_session().scalars(query).one()
    assert post.body == "test_create body"


def test_update(client: FlaskClient):
    client.post("/auth/login", data={"username": "test", "password": "test"})

    assert client.get("/1/update").status_code == 200
    client.post("/1/update", data={"title": "updated title", "body": "updated body"})

    query = select(models.Post).where(models.Post.id == 1)
    post = db.get_db_session().scalars(query).one()
    assert post.title == "updated title"
    assert post.body == "updated body"
