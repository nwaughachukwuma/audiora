import asyncio
import logging
import os
import re
import uuid
from pathlib import Path
from typing import List, Optional

from src.utils.audio_manager_utils import (
    AudioManagerConfig,
    AudioManagerSpeechGenerator,
    ContentSplitter,
    openai_voices,
)
from src.utils.audio_synthesizer import AudioSynthesizer
from src.utils.clean_tss_markup import clean_tss_markup

logger = logging.getLogger(__name__)


class AudioManager(AudioManagerSpeechGenerator, ContentSplitter):
    def __init__(self, custom_config: Optional[AudioManagerConfig] = None):
        super().__init__()

        self.config = (
            AudioManagerConfig(**custom_config.__dict__)
            if custom_config
            else AudioManagerConfig()
        )
        self.config.ensure_directories()

    def _get_tags(self, audio_script: str) -> List[str]:
        tags = re.findall(r"<(Person\d+)>", audio_script)
        tags.sort()
        return list(set(tags))

    async def generate_speech(self, audio_script: str):
        """
        Logic to make audiocast from audio script.
        Args:
            audio_script (str): Audio script to convert to speech.
        """
        output_file = f"{self.config.outdir_base}/{str(uuid.uuid4())}.mp3"
        await self.text_to_speech(audio_script, output_file)

        return output_file

    async def text_to_speech(self, audio_script: str, output_file: str):
        """
        Convert audio script to speech and save as an audio file.
        Args:
            audio_script (str): Audio script to convert to speech.
            output_file (str): path to save the output audio file.
        Raises:
            Exception: If there's an error in converting text to speech.
        """
        tags = self._get_tags(audio_script)
        audio_script = clean_tss_markup(audio_script, tags)

        if self.config.tts_provider == "openai":
            return await self.__text_to_speech_openai(audio_script, output_file, tags)
        else:
            raise Exception("Invalid TTS model specified")

    async def __text_to_speech_openai(
        self, audio_script: str, output_file: str, tags: List[str]
    ):
        try:
            nway_content = self.split_content(audio_script, tags)
            print(f"nway_content: {nway_content}")

            jobs = self._prepare_speech_jobs(
                nway_content, tags, openai_voices, self.config.temp_audio_dir
            )

            audio_files = await self._process_speech_jobs(jobs)
            if not audio_files:
                raise Exception("No audio files were generated")

            await self.__finalize(audio_files, output_file)
            logger.info(f"Audio saved to {output_file}")

        except Exception as e:
            raise Exception(f"Error converting text to speech with OpenAI: {str(e)}")

    async def __finalize(self, audio_files: List[str], output_file: str) -> None:
        """
        Merge and enhance audio files and save the final output.
        Args:
            audio_files (List[str]): List of audio files to merge.
            output_file (str): Path to save the final audio output.
        """
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
