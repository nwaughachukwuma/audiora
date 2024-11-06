from anthropic import Anthropic, AsyncAnthropic

from env_var import ANTHROPIC_API_KEY


def get_anthropic():
    """Return anthropic async client"""
    return AsyncAnthropic(api_key=ANTHROPIC_API_KEY)


def get_anthropic_sync():
    """Return anthropic sync client"""
    return Anthropic(api_key=ANTHROPIC_API_KEY)
