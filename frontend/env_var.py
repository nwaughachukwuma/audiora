from os import environ

BACKEND_URL = environ.get("BACKEND_URL", "http://localhost:8000")
APP_URL = environ.get("APP_URL", "http://localhost:8501")
