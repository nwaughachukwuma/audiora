import uuid
from pathlib import Path
from typing import Dict, List

import streamlit as st
from pydantic import BaseModel

from src.services.storage import StorageManager
from src.utils.audio_manager import AudioManager
from src.utils.audio_synthesizer import AudioSynthesizer
from src.utils.audiocast_request import AudioScriptMaker, generate_source_content
from src.utils.chat_request import chat_request
from src.utils.chat_utils import (
    SessionChatMessage,
    SessionChatRequest,
    content_categories,
)


class GenerateAudioCastRequest(BaseModel):
    summary: str
    category: str


class GenerateAudioCastResponse(BaseModel):
    uuid: str
    url: str
    script: str
    source_content: str


# Store chat sessions (in-memory for now, should be moved to a database in production)
chat_sessions: Dict[str, List[SessionChatMessage]] = {}


def chat(session_id: str, request: SessionChatRequest):
    message = request.message
    content_category = request.content_category

    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    chat_sessions[session_id].append(message)

    def on_finish(text: str):
        chat_sessions[session_id].append(
            SessionChatMessage(role="assistant", content=text)
        )
        # log text and other metadata to database

    generator = chat_request(
        content_category=content_category,
        previous_messages=chat_sessions[session_id],
        on_finish=on_finish,
    )

    return generator


async def generate_audiocast(request: GenerateAudioCastRequest):
    """
    Generate an audiocast based on a summary of user's request
    """
    summary = request.summary
    category = request.category
    if category not in content_categories:
        raise Exception("Invalid content category")

    container = st.empty()

    # TODO: We can keep the process for generating source content and audio content separate
    # STEP 1: Generate source content
    with container.container():
        container.info("Generating source content...")

        source_content = generate_source_content(category, summary)
        print(f"audiocast source content: {source_content}")
        if not source_content:
            raise Exception("Failed to develop audiocast source content")

    # STEP 2: Generate audio script
    with container.container():
        container.info("Generating audio script...")

        audio_script_maker = AudioScriptMaker(category, source_content)
        audio_script = audio_script_maker.create(provider="anthropic")
        print(f"streamlined audio_script: {audio_script}")
        if not audio_script:
            raise Exception("Error while generating audio script")

    # STEP 3: Generate audio from the audio script
    with container.container():
        container.info("Generating audio...")
        output_file = await AudioManager().generate_speech(audio_script)

        container.info("Enhancing audio quality...")
        AudioSynthesizer().enhance_audio_minimal(Path(output_file))
        print(f"output_file: {output_file}")

    # unique ID for the audiocast
    uniq_id = str(uuid.uuid4())

    # TODO: Use a background service
    # STEP 4: Ingest audio file to a storage service (e.g., GCS, S3)
    with container.container():
        try:
            container.info("Storing a copy of your audiocast...")
            storage_manager = StorageManager()
            storage_manager.upload_audio_to_gcs(output_file, uniq_id)
        except Exception as e:
            print(f"Error while storing audiocast: {str(e)}")

    response = GenerateAudioCastResponse(
        uuid=uniq_id,
        url=output_file,
        script=audio_script,
        source_content=source_content,
    )

    return response.model_dump()


async def get_audiocast_uri(uuid: str):
    """
    Get the URI for the audiocast
    """
    storage_manager = StorageManager()
    return storage_manager.download_from_gcs(uuid)
