from datetime import datetime

import pytest
from flask import Flask

from flaskr import create_app, db, models


@pytest.fixture
def app():
    database_url = "sqlite:///file:mem1?mode=memory&cache=shared&uri=True"
    app = create_app({"DATABASE_URL": database_url, "SECRET_KEY": "test"})
    with app.app_context():
        db_session = db.get_db_session()
        db.init_db(database_url)
        user_test = models.User(
            username="test",
            password="scrypt:32768:8:1$B6EWUB7sblZHpKwE$74951791e0ebcdcf91999e0e4c3e7768fcb87f994c35de0d80e99d83ec36e9f542b76c4d486c57ced5cea72fd76c3f5a64b0a2c31a89a02e3a86a52a6f52fb1c",
        )
        user_other = models.User(
            username="other",
            password="scrypt:32768:8:1$6DDdh5peSL3fmCBy$c997bb4e0ecdeb5ad2e94cd4cde3a58efa290889a7c40497b154cd23df46ffc25f731370f849ab262fd310d9ee48ce5a9950a6910e08b9a8f52ec791acb85c61",
        )
        post = models.Post(
            title="test title",
            body="test\nbody",
            author=user_test,
            created=datetime.fromisoformat("2025-01-01"),
        )
        db_session.add(user_test)
        db_session.add(user_other)
        db_session.add(post)
        db_session.commit()

        yield app


@pytest.fixture
def client(app: Flask):
    return app.test_client()
