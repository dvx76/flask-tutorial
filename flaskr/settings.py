from pathlib import Path

DATABASE_URL = f"sqlite:///{Path(__file__).parent / 'flaskr.sqlite'}"
SECRET_KEY = "dev"
