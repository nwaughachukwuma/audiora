from datetime import datetime
from pathlib import Path

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
from src.utils.session_manager import SessionManager


class GenerateAudioCastRequest(BaseModel):
    sessionId: str
    summary: str
    category: str


class GenerateAudioCastResponse(BaseModel):
    url: str
    script: str
    source_content: str
    created_at: str | None


def chat(session_id: str, request: SessionChatRequest):
    content_category = request.content_category
    db = SessionManager(session_id)
    db._add_chat(request.message)

    def on_finish(text: str):
        db._add_chat(SessionChatMessage(role="assistant", content=text))

    return chat_request(
        content_category=content_category,
        previous_messages=db._get_chats(),
        on_finish=on_finish,
    )


async def generate_audiocast(request: GenerateAudioCastRequest):
    """
    Generate an audiocast based on a summary of user's request
    """
    session_id = request.sessionId
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

    # TODO: Use a background service
    # STEP 4: Ingest audio file to a storage service (e.g., GCS, S3)
    with container.container():
        try:
            container.info("Storing a copy of your audiocast...")
            storage_manager = StorageManager()
            storage_manager.upload_audio_to_gcs(output_file, session_id)
        except Exception as e:
            print(f"Error while storing audiocast: {str(e)}")

    db = SessionManager(session_id)
    db._update_source(source_content)
    db._update_transcript(audio_script)

    response = GenerateAudioCastResponse(
        url=output_file,
        script=audio_script,
        source_content=source_content,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    return response.model_dump()


def get_audiocast(session_id: str):
    """
    Get the URI for the audiocast
    """
    storage_manager = StorageManager()
    filepath = storage_manager.download_from_gcs(session_id)

    session_data = SessionManager(session_id).data()
    if not session_data:
        raise Exception(f"Audiocast not found for session_id: {session_id}")

    metadata = session_data.metadata
    source = metadata.source if metadata else ""
    transcript = metadata.transcript if metadata else ""

    created_at: str | None = None
    if session_data.created_at:
        created_at = datetime.fromisoformat(session_data.created_at).strftime(
            "%Y-%m-%d %H:%M"
        )

    response = GenerateAudioCastResponse(
        url=filepath,
        script=transcript,
        source_content=source,
        created_at=created_at,
    )

    return response.model_dump()
