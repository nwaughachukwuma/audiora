import uuid
from datetime import datetime
from typing import Dict, List

from fastapi import HTTPException
from pydantic import BaseModel
from slugify import slugify

from src.utils.chat_request import chat_request
from src.utils.chat_utils import SessionChatMessage, SessionChatRequest


class AudioCastRequest(BaseModel):
    summary: str
    category: str


class AudioCastResponse(BaseModel):
    uuid: str
    slug: str
    audio_url: str
    transcript: str
    metadata: dict


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


async def generate_audiocast(request: AudioCastRequest):
    # Generate a unique ID for the audiocast
    audiocast_id = str(uuid.uuid4())

    # Generate slug from the query
    slug = slugify(request.summary[:50])  # First 50 chars for the slug

    # TODO: Implement content generation based on type
    if request.category == "story":
        prompt_template = "Create an engaging story about {query}"
    elif request.category == "podcast":
        prompt_template = "Create an informative podcast script about {query}"
    elif request.category == "sermon":
        prompt_template = "Create an inspiring sermon about {query}"
    elif request.category == "science":
        prompt_template = "Create an educational scientific explanation about {query}"
    else:
        raise HTTPException(status_code=400, detail="Invalid content type")

    # TODO: Implement content generation and audio synthesis
    print(f"prompt_template: {prompt_template}")

    return AudioCastResponse(
        uuid=audiocast_id,
        slug=slug,
        audio_url=f"/audio/{audiocast_id}.mp3",
        transcript="Generated transcript will go here",
        metadata={
            "category": request.category,
            "summary": request.summary,
            "created_at": datetime.now().isoformat(),
        },
    )


async def get_audiocast(uuid: str):
    # TODO: Implement audiocast retrieval
    pass
