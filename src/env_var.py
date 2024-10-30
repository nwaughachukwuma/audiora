from os import environ

from dotenv import load_dotenv

if environ.get("ENV", "local") == "local":
    load_dotenv(dotenv_path="./.env.local")
else:
    load_dotenv()

OPENAI_API_KEY = environ["OPENAI_API_KEY"]
ANTHROPIC_API_KEY = environ["ANTHROPIC_API_KEY"]
GEMINI_API_KEY = environ["GEMINI_API_KEY"]
ELEVENLABS_API_KEY = environ["ELEVENLABS_API_KEY"]

APP_URL = environ.get("APP_URL", "http://localhost:8501")
