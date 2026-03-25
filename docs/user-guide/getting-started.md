# Getting Started

This page gives you the mental model for FlaskR before you run it.

## What the app does

FlaskR supports a compact but complete blog workflow:

- Visitors can read posts on `/`.
- New users can register at `/auth/register`.
- Existing users can log in at `/auth/login`.
- Authenticated authors can create, edit, and delete their own posts.

!!! example "Typical request flow"
    1. A user submits the login form.
    2. `flaskr/auth.py` validates the credentials and stores `user_id` in the session.
    3. Before the next request, `load_logged_in_user()` loads the current user into `g.user`.
    4. Protected views use `@login_required` to reject anonymous visitors.

## Authorization in one glance

```py title="flaskr/blog.py"
def get_post(id: int) -> Post:
    post = get_db_session().get(Post, id)  # (1)!

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")  # (2)!

    assert g.user is not None
    if post.author_id != g.user.id:
        abort(403)  # (3)!

    return post
```

1. Load the post from the current request's database session.
2. Missing content becomes `404 Not Found`.
3. A different logged-in user gets `403 Forbidden` instead of edit access.

!!! note "Decorator order matters"
    In `flaskr/auth.py`, `@login_required` is placed below `@bp.route(...)`. Flask registers the route first, then the wrapper enforces authentication.

## The data model

The app only needs two tables, which is one reason it is so approachable in class.

| Model | Key fields | Purpose |
| --- | --- | --- |
| `User` | `id`, `username`, `password` | Stores registered accounts |
| `Post` | `id`, `title`, `body`, `created`, `author_id` | Stores blog posts and links them to authors |

That small schema is enough to teach basic CRUD behavior, ownership checks, and relationships without burying students in domain details.

## How to explore the repository

1. Read `flaskr/__init__.py` to understand app startup.
2. Open `flaskr/models.py` to see the data model.
3. Compare `flaskr/auth.py` and `flaskr/blog.py` to understand blueprint boundaries.
4. Run `pytest` and inspect `tests/test_auth.py` and `tests/test_blog.py` as executable documentation.[^tests]

!!! tip "Tests are part of the lesson 🚀"
    The test suite is small enough to read quickly, which makes it a useful bridge between the prose docs and the implementation.

*[CRUD]: Create, Read, Update, Delete.

[^tests]: The test fixtures use an in-memory SQLite database so students can run the suite without setting up external infrastructure.
