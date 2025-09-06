import os
from dataclasses import dataclass
from typing import List, Literal

from src.services.openai_client import get_openai
from src.utils.decorators.base import process_time

OpenaiVoice = Literal["onyx", "shimmer", "echo", "nova", "alloy", "ash", "ballad", "coral", "fable", "sage"]
openai_voices: List[OpenaiVoice] = [
    "onyx",
    "shimmer",
    "echo",
    "nova",
    "alloy",
    "ash",
    "ballad",
    "coral",
    "fable",
    "sage",
]


@dataclass
class SpeechJob:
    content: str
    voice: OpenaiVoice
    output_file: str
    tag: str
    index: int


class GenerateSpeech:
    def __init__(self):
        pass

    def run(self, job: SpeechJob):
        """Generate speech using OpenAI TTS"""
        try:
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

        # Use streaming response to write directly to a temp file then read it back
        temp_path = f"{job.output_file}.temp"
        with get_openai().audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=job.voice,
            input=job.content,
            response_format="mp3",
        ) as response:
            response.stream_to_file(temp_path)

        with open(temp_path, "rb") as f:
            content = f.read()

        if os.path.exists(temp_path):
            os.remove(temp_path)

        return content
