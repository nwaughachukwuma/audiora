from os import environ

BUCKET_NAME = environ["BUCKET_NAME"]

OPENAI_API_KEY = environ["OPENAI_API_KEY"]
ANTHROPIC_API_KEY = environ["ANTHROPIC_API_KEY"]
GEMINI_API_KEY = environ["GEMINI_API_KEY"]

REDIS_HOST = environ["REDIS_HOST"]
REDIS_PASSWORD = environ["REDIS_PASSWORD"]

APP_URL = environ.get("APP_URL", "http://localhost:8501")
API_URL = environ["API_URL"]

CSE_ID = environ["CSE_ID"]
CSE_API_KEY = environ["GOOGLE_API_KEY"]

PROD_ENV = environ.get("ENV", "dev") == "prod"
