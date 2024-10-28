import re

from src.services.gemini_client import GeminiConfig, generate_content
from src.services.openai_client import get_openai
from src.utils.chat_utils import ContentCategory
from src.utils.prompt_templates.source_content_prompt import get_content_source_prompt
from src.utils.prompt_templates.streamline_audio import streamline_audio_script_prompt
from src.utils.prompt_templates.tts_prompt import Metadata, TTSPromptMaker


def generate_source_content(category: ContentCategory, summary: str):
    """
    Generate audiocast source conntent based on a summary of the user's request

    Returns:
    str: The audiocast source content
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


def create_audio_script(category: ContentCategory, source_content: str):
    """
    Create an audio script based on the source content

    Returns:
    str: streamlined audio script
    """

    prompt_maker = TTSPromptMaker(category, Metadata())
    system_prompt = prompt_maker.get_system_prompt(source_content)

    print("Generating audio script...")

    response = get_openai().chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Now create a TTS-optimized audiocast script."},
        ],
        temperature=0.5,
        max_tokens=4096,
    )

    audio_script = response.choices[0].message.content
    print(f"Audio script generated successfully: {audio_script}")
    if not audio_script:
        raise ValueError("Failed to generate audio script")

    print("Streamlining the  audio script...")

    streamlined_script = streamline_audio_script(
        instruction=system_prompt, audio_script=audio_script
    )

    return str(streamlined_script)


def streamline_audio_script(instruction: str, audio_script: str):
    """
    Streamline the audio script to align with the specified TTS requirements.
    """
    response = generate_content(
        prompt=[
            "Now streamline the audio script to match the specified TTS requirements."
        ],
        config=GeminiConfig(
            model_name="gemini-1.5-flash-002",
            system_prompt=streamline_audio_script_prompt(instruction, audio_script),
            temperature=0.5,
            max_output_tokens=4096,
        ),
    )

    return response
