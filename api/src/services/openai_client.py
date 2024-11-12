from openai import Client

from api.src.env_var import OPENAI_API_KEY


def get_openai():
    return Client(api_key=OPENAI_API_KEY)
