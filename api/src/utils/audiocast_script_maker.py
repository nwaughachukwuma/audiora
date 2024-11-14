from typing import Literal

from src.services.anthropic_client import get_anthropic_sync
from src.services.gemini_client import GeminiConfig, generate_content
from src.services.openai_client import get_openai
from src.utils.chat_utils import ContentCategory
from src.utils.prompt_templates.streamline_audio import streamline_audio_script_prompt
from src.utils.prompt_templates.tts_prompt import Metadata, TTSPromptMaker

AudioScriptProvider = Literal["openai", "anthropic"]


class AudioScriptMaker:
    category: ContentCategory

    def __init__(
        self,
        category: ContentCategory,
        source_content: str,
    ):
        self.category = category
        self.source_content = source_content

    def create(self, provider: AudioScriptProvider = "openai"):
        """
        Create an audio script based on the source content

        Args:
            category (ContentCategory): The content category
            source_content (str): The audiocast source content
        Returns:
            str: streamlined audio script
        """
        print("Generating audio script...")
        print(f"Category: {self.category}; Source content: {self.source_content}")

        prompt_maker = TTSPromptMaker(self.category, Metadata())
        system_prompt = prompt_maker.get_system_prompt(self.source_content)

        audio_script = self.__use_openai(system_prompt) if provider == "openai" else self.__use_anthropic(system_prompt)

        print(f"Audio script generated successfully: {audio_script}")
        if not audio_script:
            raise ValueError("Failed to generate audio script")

        print("Streamlining the  audio script...")

        streamlined_script = self.streamline_audio_script(instruction=system_prompt, audio_script=audio_script)

        return str(streamlined_script)

    def __use_openai(self, system_prompt: str):
        response = get_openai().chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": "Now create a TTS-optimized audiocast script.",
                },
            ],
            temperature=0.3,
            max_tokens=7120,
        )

        return response.choices[0].message.content

    def __use_anthropic(self, system_prompt: str):
        result = get_anthropic_sync().messages.create(
            model="claude-3-5-sonnet-20241022",
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": "Now create a TTS-optimized audiocast script.",
                },
            ],
            temperature=0.3,
            max_tokens=7120,
        )

        return "".join(item.text for item in result.content if item.type == "text")

    def streamline_audio_script(self, instruction: str, audio_script: str):
        """
        Streamline the audio script to align with the specified TTS requirements.

        Args:
            instruction (str): The TTS requirements
            audio_script (str): The generated audio script
        Returns:
            str: The streamlined audio script
        """
        response = generate_content(
            prompt=["Now streamline the audio script to match the specified TTS requirements."],
            config=GeminiConfig(
                model_name="gemini-1.5-flash-002",
                system_prompt=streamline_audio_script_prompt(instruction, audio_script),
                temperature=0.1,
                max_output_tokens=7120,
            ),
        )

        return response
