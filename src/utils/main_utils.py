import uuid
from pathlib import Path
from typing import Dict, List

import streamlit as st
from fastapi import HTTPException
from pydantic import BaseModel
from slugify import slugify

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
    slug: str
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
        raise HTTPException(status_code=400, detail="Invalid content category")

    container = st.empty()

    # TODO: We can keep the process for generating source content and audio content separate
    # STEP 1: Generate source content
    with container.container():
        container.info("Generating source content...")

        source_content = generate_source_content(category, summary)
        print(f"audiocast source content: {source_content}")
        if not source_content:
            raise HTTPException(
                status_code=500, detail="Failed to develop audiocast source content"
            )

    # STEP 2: Generate audio script
    with container.container():
        container.info("Generating audio script...")

        audio_script_maker = AudioScriptMaker(category, source_content)
        audio_script = audio_script_maker.create(provider="anthropic")
        print(f"streamlined audio_script: {audio_script}")
        if not audio_script:
            raise HTTPException(
                status_code=500, detail="Error while generating audio script"
            )

    # TODO: Ingest audio file to a storage service (e.g., GCS, S3) using a background service
    # STEP 3: Generate audio from the audio script
    with container.container():
        container.info("Generating audio...")
        outputfile = await AudioManager().generate_speech(audio_script)

        container.info("Enhancing audio quality...")
        AudioSynthesizer().enhance_audio(Path(outputfile))
        print(f"outputfile: {outputfile}")

    # Generate slug from the query
    slug = slugify((category + summary)[:50])  # First 50 chars for the slug
    # Generate a unique ID for the audiocast
    audiocast_id = str(uuid.uuid4())

    response = GenerateAudioCastResponse(
        uuid=audiocast_id,
        slug=slug,
        url=outputfile,
        script=audio_script,
        source_content=source_content,
    )

    return response.model_dump()


async def get_audiocast(uuid: str):
    # TODO: Implement audiocast retrieval
    pass
