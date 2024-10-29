import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from functools import partial
from itertools import cycle, islice
from pathlib import Path
from typing import Any, List, Literal, Optional, Tuple

from src.services.openai_client import get_openai

logger = logging.getLogger(__name__)
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
class AudioCasterConfig:
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

            logger.debug(f"Generated speech for tag {job.tag} at index {job.index}")
            return job.output_file
        except Exception as e:
            logger.error(f"Failed to generate speech for tag {job.tag}: {str(e)}")
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
