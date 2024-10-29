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

OpenaiVoice = Literal["echo", "shimmer", "onyx", "nova", "alloy"]
openai_voices: List[OpenaiVoice] = ["echo", "shimmer", "onyx", "nova", "alloy"]


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
        nway_content: List[Tuple[str, ...]],
        tags: List[str],
        voices: List[Any],
        temp_audio_dir: str,
    ):
        jobs: List[SpeechJob] = []
        counter = 0
        # Create tag-to-voice mapping
        voice_mapping = self._create_voice_mapping(tags, voices)

        for dialogue_parts in nway_content:
            for tag, content_part in zip(tags, dialogue_parts):
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
    def split_content(self, content: str, tags: List[str]) -> List[Tuple[str, ...]]:
        """
        Split text content into n-way dialogues based.
        Args:
            content (str): Audio script containing tagged dialogues
            tags (List[str]): List of tags to match (e.g., ["Tag1", "Tag2"])
        Returns:
            List[Tuple[str, ...]]: List of tuples containing dialogues for each tag
        Example:
            Input: "<Tag1>Hello</Tag1><Tag2>Hi</Tag2>"
            Output: [("Hello", "Hi")]
        """
        print(f"Processing script with tags: {tags}")

        if not self.validate_content(content, tags):
            raise Exception("Content does not contain proper tag structure")

        # Extract content for each tag separately
        tag_contents: List[List[str]] = []

        for tag in tags:
            pattern = f"<{tag}>(.*?)</{tag}>"
            matches = re.findall(pattern, content, re.DOTALL)

            # Clean up matches
            cleaned_matches = [" ".join(m.split()).strip() for m in matches]
            tag_contents.append(cleaned_matches)

            print(f"Found {len(cleaned_matches)} matches for tag {tag}")

        # Validate we have content
        if not any(tag_contents):
            print("No content found for any tags")
            return []

        # Get the last tag where there's a mismatch in speaker tags represented
        lengths = [len(content) for content in tag_contents]
        last_tag_content = tag_contents[-1] if len(set(lengths)) > 1 else None

        # Zip the contents together
        zipped = list(zip(*tag_contents))
        if last_tag_content:
            zipped.append(tuple(last_tag_content))

        print(f"Generated {tag_contents} dialogue tags. Zipped: {zipped}")
        return zipped

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
