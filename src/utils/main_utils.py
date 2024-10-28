import uuid
from typing import Dict, List

from fastapi import HTTPException
from pydantic import BaseModel
from slugify import slugify

from src.utils.audiocast_request import create_audio_script, generate_source_content
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

    source_content = generate_source_content(category, summary)
    print(f"audiocast source content: {source_content}")
    if not source_content:
        raise HTTPException(
            status_code=500, detail="Failed to develop audiocast source content"
        )

    audio_script = create_audio_script(category, source_content)
    print(f"streamliend audio_script: {audio_script}")
    if not audio_script:
        raise HTTPException(
            status_code=500, detail="Error while generating audio script"
        )

    # Generate slug from the query
    slug = slugify((category + summary)[:50])  # First 50 chars for the slug
    # Generate a unique ID for the audiocast
    audiocast_id = str(uuid.uuid4())

    response = GenerateAudioCastResponse(
        uuid=audiocast_id,
        slug=slug,
        url=f"/audio/{audiocast_id}.mp3",
        script=audio_script,
        source_content=source_content,
    )

    return response.model_dump()


async def get_audiocast(uuid: str):
    # TODO: Implement audiocast retrieval
    pass
