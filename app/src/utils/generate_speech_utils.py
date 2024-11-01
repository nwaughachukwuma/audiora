from dataclasses import dataclass
from io import BytesIO
from typing import Dict, List, Literal

from src.services.elevenlabs_client import get_elevenlabs_client
from src.services.openai_client import get_openai
from src.utils.decorators import process_time

TTSProvider = Literal["openai", "elevenlabs"]

OpenaiVoice = Literal["onyx", "shimmer", "echo", "nova", "alloy"]
openai_voices: List[OpenaiVoice] = ["onyx", "shimmer", "echo", "nova", "alloy"]

ElevenLabsVoice = Literal[
    "Adam", "Sarah", "Laura", "Charlie", "George", "Charlotte", "Liam"
]
elevenlabs_voices: List[ElevenLabsVoice] = [
    "Adam",
    "Sarah",
    "Laura",
    "Charlie",
    "George",
    "Charlotte",
    "Liam",
]

elevenlabs_voice_to_id: Dict[ElevenLabsVoice, str] = {
    "Adam": "pNInz6obpgDQGcFmaJgB",
    "Sarah": "EXAVITQu4vr4xnSDxMaL",
    "Laura": "FGY2WhTYpPnrIDTdsKH5",
    "Charlie": "IKne3meq5aSn9XLyUdCD",
    "George": "JBFqnCBsd6RMkjVDRZzb",
    "Charlotte": "XB0fDUnXU5powFXDhCwa",
    "Liam": "TX3LPaxmHKxFdv7VOQHJ",
}


@dataclass
class SpeechJob:
    content: str
    voice: OpenaiVoice | ElevenLabsVoice
    output_file: str
    tag: str
    index: int


class GenerateSpeech:
    provider: TTSProvider

    def __init__(self, provider: TTSProvider):
        self.provider = provider

    def run(self, job: SpeechJob):
        """Generate speech using the specified provider"""
        try:
            if self.provider == "elevenlabs":
                content = self.__use_elevenlabs(job)
            else:
                content = self.__use_openai(job)

            with open(job.output_file, "wb") as file:
                file.write(content)

            print(f"Generated speech for tag {job.tag} at index {job.index}")
            return job.output_file
        except Exception as e:
            print(f"Failed to generate speech for tag: {job.tag}. Error: {str(e)}")
            return ""

    @process_time()
    def __use_openai(self, job: SpeechJob):
        if job.voice not in openai_voices:
            raise ValueError("Wrong voice specification for openai tts")

        response = get_openai().audio.speech.create(
            input=job.content, model="tts-1-hd", voice=job.voice
        )
        return response.content

    @process_time()
    def __use_elevenlabs(self, job: SpeechJob):
        if job.voice not in elevenlabs_voices:
            raise ValueError("Wrong voice specification for elevenlabs tts")
        # response = get_elevenlabs_client().text_to_speech.convert(
        #     model_id="eleven_turbo_v2_5", # use the turbo model for low latency
        #     text=job.content,
        #     voice_id=elevenlabs_voice_to_id[job.voice],
        #     output_format="mp3_22050_32",
        # )
        response = get_elevenlabs_client().generate(
            model="eleven_multilingual_v2",
            text=job.content,
            voice=job.voice,
        )

        buffer = BytesIO()
        for chunk in response:
            if chunk:
                buffer.write(chunk)

        buffer.seek(0)
        return buffer.getvalue()
