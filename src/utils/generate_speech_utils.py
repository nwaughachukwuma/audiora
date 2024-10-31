from dataclasses import dataclass
from io import BytesIO
from typing import List, Literal

from elevenlabs import VoiceSettings

from src.services.elevenlabs_client import get_elevenlabs_client
from src.services.openai_client import get_openai

TTSProvider = Literal["openai", "elevenlabs"]
OpenaiVoice = Literal["onyx", "shimmer", "echo", "nova", "alloy"]
openai_voices: List[OpenaiVoice] = ["onyx", "shimmer", "echo", "nova", "alloy"]

ElevenLabsVoice = Literal[
    "Adam", "Sarah", "Laura", "Charlie", "George", "Charlotte", "Liam"
]
elevenlabs_voices = ["Adam", "Sarah", "Laura", "Charlie", "George", "Charlotte", "Liam"]


@dataclass
class SpeechJob:
    content: str
    voice: OpenaiVoice
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
            content = (
                self.__use_openai(job)
                if self.provider == "elevenlabs"
                else self.__use_elevenlabs(job)
            )

            with open(job.output_file, "wb") as file:
                file.write(content)

            print(f"Generated speech for tag {job.tag} at index {job.index}")
            return job.output_file
        except Exception as e:
            print(f"Failed to generate speech for tag {job.tag}: {str(e)}")
            return ""

    def __use_openai(self, job: SpeechJob):
        response = get_openai().audio.speech.create(
            input=job.content, model="tts-1-hd", voice=job.voice
        )
        return response.content

    def __use_elevenlabs(self, job: SpeechJob):
        response = get_elevenlabs_client().text_to_speech.convert(
            voice_id=job.voice,
            output_format="mp3_22050_32",
            text=job.content,
            model_id="eleven_turbo_v2_5",  # use the turbo model for low latency
            voice_settings=VoiceSettings(
                stability=0.0, similarity_boost=1.0, style=0.0, use_speaker_boost=True
            ),
        )

        buffer = BytesIO()
        for chunk in response:
            if chunk:
                buffer.write(chunk)

        buffer.seek(0)
        return buffer.getvalue()
