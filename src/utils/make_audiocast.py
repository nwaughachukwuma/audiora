import re

from src.services.gemini_client import GeminiConfig, generate_content
from src.services.openai_client import get_openai
from src.utils.chat_utils import ContentCategory
from src.utils.prompt_templates.source_content_prompt import get_content_source_prompt
from src.utils.prompt_templates.streamline_audio import streamline_audio_script_prompt
from src.utils.prompt_templates.tts_prompt import Metadata, TTSPromptMaker


def generate_audiocast_source(category: ContentCategory, summary: str):
    """
    Generate an audiocast source based on a summary of user's request
    """
    refined_summary = re.sub(
        "You want", "a user who wants", summary, flags=re.IGNORECASE
    )
    refined_summary = re.sub("You", "a user", refined_summary, flags=re.IGNORECASE)

    response = get_openai().chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": get_content_source_prompt(category, refined_summary),
            },
            {"role": "user", "content": "Now develop content."},
        ],
        temperature=0.5,
        max_tokens=4096,
    )

    return response.choices[0].message.content


def structure_content_to_tts(category: ContentCategory, source_content: str):
    """
    Structure the content to a more streamlined form
    """

    prompt_maker = TTSPromptMaker(category, Metadata())

    response = get_openai().chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": prompt_maker.get_system_prompt(source_content),
            },
            {"role": "user", "content": "Now create a TTS-optimized audiocast script."},
        ],
        temperature=0.5,
        max_tokens=4096,
    )

    return response.choices[0].message.content


def streamline_audio_script(tts_prompt: str, audio_script: str):
    """
    Streamline the audio script to align with the specified TTS requirements.
    """
    response = generate_content(
        prompt=[
            "Now streamline the audio script to match the specified TTS requirements."
        ],
        config=GeminiConfig(
            model_name="gemini-1.5-flash-002",
            system_prompt=streamline_audio_script_prompt(tts_prompt, audio_script),
            temperature=0.5,
            max_output_tokens=4096,
        ),
    )

    return response
