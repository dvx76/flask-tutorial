# Welcome to FlaskR

Meer weten over [`create_app`](reference.md#flaskr.create_app){ data-preview }.

=== "Install with `uv`"

    Run this:

    ```bash
    uv add flask
    ```

=== "Install with `pip`"

    Run this:

    ```bash
    pip install flask
    ```


```python title="flaskr/__init__.py" linenums="1" hl_lines="6-9 15"
def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object("flaskr.settings")  # (1)!
    app.config.from_envvar("FLASKR_SETTINGS", silent=True)  # (2)!

    db_session, remove_session = db.create_db_session(
        app.config["DATABASE_URL"]
    )
    app.config["DB_SESSION"] = db_session

    app.teardown_appcontext(remove_session)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    return app
```

1. Load the default values from `flaskr/settings.py`.
2. Optionally override them with the `FLASKR_SETTINGS` environment variable.

FlaskR is a compact teaching app based on the official Flask tutorial. (1)
{ .annotate }

1.  The **tutorial** can be found [here](https://flask.palletsprojects.com/en/stable/tutorial/).

!!! note

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

!!! note

    Admonitions kunnen je documentatie sterker en gebruiksvriendelijker maken.
    Maar overdrijf niet in hun gebruik!
