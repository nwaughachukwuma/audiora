import logging
import os
import re
import uuid
from dataclasses import dataclass, field
from itertools import cycle, islice
from pathlib import Path
from typing import List, Literal, Optional, Tuple

from src.services.openai_client import get_openai
from src.utils.audio_synthesizer import AudioSynthesizer
from src.utils.clean_tss_markup import clean_tss_markup

logger = logging.getLogger(__name__)

OpenaiVoice = Literal["echo", "shimmer", "onyx", "nova", "alloy"]
openai_voices: List[OpenaiVoice] = ["echo", "shimmer", "onyx", "nova", "alloy"]


@dataclass
class Config:
    tts_provider: Optional[Literal["openai"]] = "openai"
    temp_audio_dir: str = field(default_factory=lambda: "/tmp/audiocast")
    outdir_base: str = field(default_factory=lambda: "/tmp/audiocast/output")

    def ensure_directories(self) -> None:
        """Ensure all required directories exist"""
        for directory in [self.temp_audio_dir, self.outdir_base]:
            Path(directory).mkdir(parents=True, exist_ok=True)


class AudioCaster:
    def __init__(self, custom_config: Optional[Config] = None):
        self.config = Config(**custom_config.__dict__) if custom_config else Config()
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
            print(nway_content)

            # Create voice cycle for n-way distribution
            available_voices = openai_voices[: len(tags)]  # Limit to number of tags
            if len(available_voices) < len(tags):
                available_voices = list(islice(cycle(openai_voices), len(tags)))

            # Create tag-to-voice mapping
            voice_mapping = dict(zip(tags, available_voices))
            audio_files = []
            counter = 0

            for dialogue_parts in nway_content:
                for tag, content_part in zip(tags, dialogue_parts):
                    if not content_part.strip():
                        continue

                    counter += 1
                    file_name = f"{self.config.temp_audio_dir}/{counter}.mp3"

                    # Generate the speech
                    response = get_openai().audio.speech.create(
                        input=content,
                        model="tts-1-hd",
                        voice=voice_mapping[tag],
                    )

                    with open(file_name, "wb") as file:
                        file.write(response.content)

                    audio_files.append(file_name)

            synthesizer = AudioSynthesizer(output_dir=self.config.outdir_base)
            synthesizer.merge_audio_files(self.config.temp_audio_dir, output_file)
            synthesizer.enhance_audio(Path(output_file))

            # Clean up individual audio files
            for file in audio_files:
                os.remove(file)

            logger.info(f"Audio saved to {output_file}")

        except Exception as e:
            raise Exception(f"Error converting text to speech with OpenAI: {str(e)}")
