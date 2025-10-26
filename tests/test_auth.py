import pytest
from flask import g, session
from flask.testing import FlaskClient
from sqlalchemy import select

from flaskr import db, models


def test_register_get(client: FlaskClient):
    response = client.get("/auth/register")

    assert response.status_code == 200


def test_register_post(client: FlaskClient):
    response = client.post("/auth/register", data={"username": "a", "password": "a"})

    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"

    query = select(models.User).where(models.User.username == "a")
    assert db.get_db_session().execute(query).one_or_none() is not None


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("test", "", b"Password is required."),
        ("test", "test", b"already registered"),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert message in response.data


def test_login(client):
    assert client.get("/auth/login").status_code == 200
    response = client.post("/auth/login", data={"username": "test", "password": "test"})
    assert response.headers["Location"] == "/"

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user.username == "test"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("a", "test", "Incorrect username."),
        ("test", "a", "Incorrect password."),
    ),
)
def test_login_validate_input(client, username, password, message):
    response = client.post(
        "/auth/login", data={"username": username, "password": password}
    )
    assert message in response.text


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
    ),
)
def test_create_update_validate(client: FlaskClient, path: str):
    client.post("/auth/login", data={"username": "test", "password": "test"})

    response = client.post(path, data={"title": "", "body": "invalid post"})
    assert b"Title is required." in response.data

    query = select(models.Post).where(models.Post.body == "invalid post")
    assert db.get_db_session().execute(query).one_or_none() is None


def test_delete(client: FlaskClient):
    client.post("/auth/login", data={"username": "test", "password": "test"})

    response = client.post("/1/delete")
    assert response.headers["Location"] == "/"

    query = select(models.Post).where(models.Post.id == 1)
    assert db.get_db_session().execute(query).one_or_none() is None
