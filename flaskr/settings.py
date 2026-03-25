"""Default configuration values for the tutorial application.

These settings keep the example project runnable out of the box while still
being easy to override in tests, local environment files, or deployment
configuration.
"""

from pathlib import Path

DATABASE_URL: str = f"sqlite:///{Path(__file__).parent / 'flaskr.sqlite'}"
SECRET_KEY: str = "dev"
