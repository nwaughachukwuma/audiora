import asyncio
import logging
import os
import re
import uuid
from pathlib import Path
from typing import List, Optional, Tuple

from src.utils.audio_manager_utils import (
    AudioManagerConfig,
    AudioManagerSpeechGenerator,
    ContentSplitter,
)
from src.utils.audio_synthesizer import AudioSynthesizer
from src.utils.clean_tss_markup import clean_tss_markup
from src.utils.generate_speech_utils import elevenlabs_voices, openai_voices

logger = logging.getLogger(__name__)


class AudioManager(AudioManagerSpeechGenerator, ContentSplitter):
    def __init__(self, custom_config: Optional[AudioManagerConfig] = None):
        super().__init__()

        self.config = AudioManagerConfig(**custom_config.__dict__) if custom_config else AudioManagerConfig()
        self.config.ensure_directories()

    def _get_ssml_tags(self) -> List[str]:
        if self.config.tts_provider == "openai":
            return []
        elif self.config.tts_provider == "elevenlabs":
            return ["say-as", "emphasis", "phoneme", "prosody", "break"]
        else:
            return []

    def _get_speaker_tags(self, audio_script: str):
        tags: List[str] = re.findall(r"<(Speaker\d+)>", audio_script)
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
        tags = self._get_speaker_tags(audio_script)
        ssml_tags = self._get_ssml_tags()

        audio_script = clean_tss_markup(audio_script, tags + ssml_tags)
        nway_content = self.split_content(audio_script, tags)

        print(f"nway_content: {nway_content}")

        if self.config.tts_provider == "elevenlabs":
            try:
                audio_files = await self.__text_to_speech_elevenlabs(nway_content, tags)
            except Exception as e:
                logger.warning(f"ElevenLabs TTS failed: {str(e)}. Falling back to OpenAI")
                self.config.tts_provider = "openai"
                return await self.text_to_speech(audio_script, output_file)
        elif self.config.tts_provider == "openai":
            audio_files = await self.__text_to_speech_openai(nway_content, tags)
        else:
            raise Exception("Invalid TTS model specified")

        if not audio_files:
            raise Exception("No audio files were generated")

        await self.__finalize(audio_files, output_file)
        logger.info(f"Audio saved to {output_file}")

    async def __text_to_speech_openai(self, nway_content: List[Tuple[str, str]], tags: List[str]) -> List[str]:
        try:
            jobs = self._prepare_speech_jobs(nway_content, tags, openai_voices, self.config.temp_audio_dir)

            return await self._process_speech_jobs(jobs, provider="openai")
        except Exception as e:
            raise Exception(f"Error converting text to speech with OpenAI: {str(e)}")

    async def __text_to_speech_elevenlabs(self, nway_content: List[Tuple[str, str]], tags: List[str]) -> List[str]:
        try:
            jobs = self._prepare_speech_jobs(nway_content, tags, elevenlabs_voices, self.config.temp_audio_dir)
            return await self._process_speech_jobs(jobs, provider="elevenlabs")
        except Exception as e:
            raise Exception(f"Error converting text to speech with Elevenlabs: {str(e)}")

    async def __finalize(self, audio_files: List[str], output_file: str, enhance_audio=False) -> None:
        """
        Merge and enhance audio files and save the final output.
        - Run audio processing in thread pool to avoid blocking
        Args:
            audio_files (List[str]): List of audio files to merge.
            output_file (str): Path to save the final audio output.
        """
        try:
            synthesizer = AudioSynthesizer()
            await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: synthesizer.merge_audio_files(self.config.temp_audio_dir, output_file),
            )
            if enhance_audio:
                await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    lambda: synthesizer.enhance_audio_minimal(Path(output_file)),
                )
        finally:
            for file in audio_files:
                if os.path.exists(file):
                    os.remove(file)
