from elevenlabs.client import ElevenLabs

from env_var import ELEVENLABS_API_KEY

client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)


def get_elevenlabs_client():
    return client
