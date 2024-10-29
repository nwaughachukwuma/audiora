import asyncio
import logging
import os
import re
import uuid
from pathlib import Path
from typing import List, Optional, Tuple

from src.utils.audio_manager_utils import (
    AudioCasterConfig,
    AudioManagerSpeechGenerator,
    openai_voices,
)
from src.utils.audio_synthesizer import AudioSynthesizer
from src.utils.clean_tss_markup import clean_tss_markup

logger = logging.getLogger(__name__)


class AudioCaster(AudioManagerSpeechGenerator):
    def __init__(self, custom_config: Optional[AudioCasterConfig] = None):
        super().__init__()

        self.config = (
            AudioCasterConfig(**custom_config.__dict__)
            if custom_config
            else AudioCasterConfig()
        )
        self.config.ensure_directories()

    def __get_tags(self, content: str) -> List[str]:
        tags = re.findall(r"<(Person\d+)>", content)
        return list(set(tags))

    async def run(self, content: str):
        """
        Logic to make audiocast audio content
        Args:
            content (str): Audio content to convert to speech.
        """
        output_file = f"{self.config.outdir_base}/{str(uuid.uuid4())}.mp3"
        await self.convert_to_speech(content, output_file)

        return output_file

    def split_content(self, content: str, tags: List[str]) -> List[Tuple[str, ...]]:
        """
        Split the input text into n-way dialogues based on the provided content.
        Args:
            content (str): Audio content containing tagged, Tag1, Tag2,..., TagN, dialogues.
        Returns:
            List[Tuple[str, ...]]: List of tuples containing dialogues for present speakers.
        """
        # Regular expression pattern to match Tag0, Tag1, ..., TagN speaker dialogues
        pattern = "\\s*".join([f"<{tag}>(.*?)</{tag}>" for tag in tags])
        matches = re.findall(rf"{pattern}", content, re.DOTALL)
        # Process the matches to remove extra whitespace and newlines
        return [
            tuple(" ".join(part.split()).strip() for part in match) for match in matches
        ]

    async def convert_to_speech(self, content: str, output_file: str) -> None:
        """
        Convert audio content to speech and save as an audio file.
        Args:
            content (str): Audio content to convert to speech.
            output_file (str): path to save the output audio file.
        Raises:
            Exception: If there's an error in converting text to speech.
        """
        cleaned_content = clean_tss_markup(content)

        if self.config.tts_provider == "openai":
            await self.__convert_to_speech_openai(cleaned_content, output_file)
        else:
            raise Exception("Invalid TTS model specified")

    async def __convert_to_speech_openai(self, content: str, output_file: str) -> None:
        try:
            tags = self.__get_tags(content)
            nway_content = self.split_content(content, tags)
            print(f"nway_content: {nway_content}")

            jobs = self._prepare_speech_jobs(
                nway_content, tags, openai_voices, self.config.temp_audio_dir
            )

            audio_files = await self._process_speech_jobs(jobs)
            if not audio_files:
                raise Exception("No audio files were generated")

            await self.__finalize_audio(audio_files, output_file)
            logger.info(f"Audio saved to {output_file}")

        except Exception as e:
            raise Exception(f"Error converting text to speech with OpenAI: {str(e)}")

    async def __finalize_audio(self, audio_files: List[str], output_file: str) -> None:
        try:
            synthesizer = AudioSynthesizer(output_dir=self.config.outdir_base)
            # Run audio processing in thread pool to avoid blocking
            await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: synthesizer.merge_audio_files(
                    self.config.temp_audio_dir, output_file
                ),
            )

            await asyncio.get_event_loop().run_in_executor(
                self.executor, lambda: synthesizer.enhance_audio(Path(output_file))
            )
        finally:
            for file in audio_files:
                if os.path.exists(file):
                    os.remove(file)
