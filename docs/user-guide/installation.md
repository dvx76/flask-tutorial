# FlaskR Installation

Use this page to get the app and documentation running locally.

## Prerequisites

- Python 3.13 or newer
- A virtual environment tool such as `venv`
- Optional: `uv` if you want a faster install workflow

## Install dependencies

=== "pip"

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -e .
    python -m pip install mkdocs mkdocs-material "mkdocstrings[python]"
    ```

=== "uv"

    ```bash
    uv venv
    source .venv/bin/activate
    uv pip install -e .
    uv pip install mkdocs mkdocs-material "mkdocstrings[python]"
    ```

## Initialize the local database

```bash
python -m flaskr.db
```

!!! warning "This command resets the schema"
    `flaskr.db.init_db()` drops existing tables before recreating them. That is convenient for demos and tests, but it is not something you would run against important data.

## Run the app

```bash
flask --app flaskr run --debug
```

Open `http://127.0.0.1:5000/` to see the blog.

## Run the docs site

```bash
mkdocs serve
```

Open `http://127.0.0.1:8000/` to preview the Material for MkDocs site.

## Useful commands

```bash
pytest
mkdocs build --strict
```

!!! tip "Configuration overrides"
    `create_app()` reads the `FLASKR_SETTINGS` environment variable if it is set. That makes it easy to swap in a different database URL or secret key for a demo, a test, or a classroom exercise.[^settings]

[^settings]: In other words, the checked-in defaults are only the starting point, not the only way to run the app.
