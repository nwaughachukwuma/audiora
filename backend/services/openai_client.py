from env_var import OPENAI_API_KEY
from openai import AsyncClient


def get_openai():
    return AsyncClient(api_key=OPENAI_API_KEY)
