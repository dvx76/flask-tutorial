# About FlaskR

FlaskR is a small multi-user blog written in Python with [Flask](https://flask.palletsprojects.com). The project exists to support workshops and classes where students need a codebase that is realistic, readable, and easy to document.

## Why this repository exists

- It is small enough to explore in a single lesson.
- It still covers the important pieces of a web app: routing, sessions, persistence, validation, and authorization.
- It gives documentation examples that map directly to source files students can open and inspect.

!!! note "Deliberately simple"
    FlaskR favors readability over production complexity. For example, it uses SQLite by default, keeps the model layer tiny, and focuses on the core blog workflow instead of extra platform features.

## Project map

| Area | Path | Role in the app |
| --- | --- | --- |
| Application factory | `flaskr/__init__.py` | Creates the Flask app, loads config, and registers blueprints |
| Authentication | `flaskr/auth.py` | Handles registration, login, logout, and route protection |
| Blog | `flaskr/blog.py` | Lists posts and implements create, update, and delete actions |
| Database | `flaskr/db.py` | Creates the SQLAlchemy session and initializes the schema |
| Models | `flaskr/models.py` | Defines the `User` and `Post` tables through the ORM |
| Tests | `tests/` | Documents expected behavior for auth, permissions, and post workflows |

## Documentation strategy 📝

This site intentionally mixes two styles of documentation:

1. The user guide explains how the application works and how to run it.
2. The reference section is generated from docstrings with `mkdocstrings`, so the API pages stay close to the code.[^reference]

!!! tip "Good classroom exercise"
    Update a docstring in `flaskr/blog.py`, rebuild the docs, and compare the new generated output with the narrative pages. It is an easy way to show the difference between tutorial docs and reference docs.

*[ORM]: Object-relational mapper used to map Python classes to database tables.

[^reference]: The generated reference starts from `docs/reference.md`, which points `mkdocstrings` at the `flaskr` package.
