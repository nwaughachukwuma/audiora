import asyncio
import os
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from functools import partial
from itertools import cycle, islice
from pathlib import Path
from typing import Any, List, Literal, Optional, Tuple

from src.services.openai_client import get_openai

OpenaiVoice = Literal["onyx", "shimmer", "echo", "nova", "alloy"]
openai_voices: List[OpenaiVoice] = ["onyx", "shimmer", "echo", "nova", "alloy"]


@dataclass
class SpeechJob:
    content: str
    voice: OpenaiVoice
    output_file: str
    tag: str
    index: int


@dataclass
class AudioManagerConfig:
    tts_provider: Optional[Literal["openai"]] = "openai"
    temp_audio_dir: str = field(default_factory=lambda: "/tmp/audiocast")
    outdir_base: str = field(default_factory=lambda: "/tmp/audiocast/output")

    def ensure_directories(self) -> None:
        """Ensure all required directories exist"""
        for directory in [self.temp_audio_dir, self.outdir_base]:
            Path(directory).mkdir(parents=True, exist_ok=True)


class AudioManagerSpeechGenerator:
    def __init__(self) -> None:
        self.executor = ThreadPoolExecutor(max_workers=3)

    def _create_voice_mapping(self, tags: List[str], voices: List[Any]):
        """Create mapping of tags to voices"""
        available_voices = voices[: len(tags)]
        if len(available_voices) < len(tags):
            available_voices = list(islice(cycle(voices), len(tags)))
        return dict(zip(tags, available_voices))

    def _prepare_speech_jobs(
        self,
        nway_content: List[Tuple[str, str]],
        tags: List[str],
        voices: List[Any],
        temp_audio_dir: str,
    ):
        jobs: List[SpeechJob] = []
        counter = 0
        # Create tag-to-voice mapping
        voice_mapping = self._create_voice_mapping(tags, voices)

        for tag, content_part in nway_content:
            if not content_part.strip():
                continue
            counter += 1
            file_name = f"{temp_audio_dir}/{counter}.mp3"
            jobs.append(
                SpeechJob(
                    content=content_part,
                    voice=voice_mapping[tag],
                    output_file=file_name,
                    tag=tag,
                    index=counter,
                )
            )

        return jobs

    def _generate_speech(self, job: SpeechJob) -> str:
        try:
            response = get_openai().audio.speech.create(
                input=job.content,
                model="tts-1-hd",
                voice=job.voice,
            )

            with open(job.output_file, "wb") as file:
                file.write(response.content)

            print(f"Generated speech for tag {job.tag} at index {job.index}")
            return job.output_file
        except Exception as e:
            print(f"Failed to generate speech for tag {job.tag}: {str(e)}")
            return ""

    async def _process_speech_jobs(self, jobs: List[SpeechJob]) -> List[str]:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(self.executor, partial(self._generate_speech, job))
            for job in jobs
        ]

        results = await asyncio.gather(*tasks)
        audio_files = [f for f in results if f and os.path.exists(f)]
        return audio_files


class ContentSplitter:
    def split_content(self, content: str, tags: List[str]) -> List[Tuple[str, str]]:
        """
        Split the input text into n-way dialogues based on the provided content.
        Args:
            content (str): Audio content containing tagged, Tag1, Tag2,..., TagN, dialogues.
            tags (List[str]): List of tags to split the content
        Returns:
            List[Tuple[str, str]]: List of tuples containing dialogues for present speakers.
        """
        if not self.validate_content(content, tags):
            raise Exception("Content does not contain proper tag structure")

        # Regular expression pattern to match Tag0, Tag1, ..., TagN speaker dialogues
        matches = re.findall(r"<(Person\d+)>(.*?)</Person\d+>", content, re.DOTALL)
        return [
            (str(person), " ".join(content.split()).strip())
            for person, content in matches
        ]

    @staticmethod
    def validate_content(content: str, tags: List[str]) -> bool:
        """
        Validate that the content contains proper tag structure.
        Args:
            content (str): Content to validate
            tags (List[str]): List of tags to check
        Returns:
            bool: True if content is valid, False otherwise
        """
        for tag in tags:
            # Count opening and closing tags
            opening_count = content.count(f"<{tag}>")
            closing_count = content.count(f"</{tag}>")
            if opening_count != closing_count:
                print(
                    f"Mismatched tags for {tag}: "
                    f"{opening_count} opening, {closing_count} closing"
                )
                return False

            if opening_count == 0:
                print(f"No instances of tag {tag} found")
                return False

        return True
