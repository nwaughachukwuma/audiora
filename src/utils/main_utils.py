import uuid
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import HTTPException
from pydantic import BaseModel
from slugify import slugify

from src.utils.chat_request import chat_request
from src.utils.chat_utils import ChatMessage, SessionChatRequest


class AudioCastRequest(BaseModel):
    query: str
    type: str  # 'story', 'podcast', 'sermon', 'science'
    chat_history: Optional[List[ChatMessage]] = []


class AudioCastResponse(BaseModel):
    uuid: str
    slug: str
    audio_url: str
    transcript: str
    metadata: dict


# Store chat sessions (in-memory for now, should be moved to a database in production)
chat_sessions: Dict[str, List[ChatMessage]] = {}


def chat(session_id: str, request: SessionChatRequest):
    message = request.message
    content_type = request.content_type

    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    chat_sessions[session_id].append(message)

    def on_finish(text: str):
        chat_sessions[session_id].append(ChatMessage(role="assistant", content=text))
        print(f"{session_id}: {text}; Len: {len(chat_sessions[session_id])}")

    generator = chat_request(
        content_type=content_type,
        previous_messages=chat_sessions[session_id],
        on_finish=on_finish,
    )

    return generator


async def generate_audiocast(request: AudioCastRequest):
    # Generate a unique ID for the audiocast
    audiocast_id = str(uuid.uuid4())

    # Generate slug from the query
    slug = slugify(request.query[:50])  # First 50 chars for the slug

    # TODO: Implement content generation based on type
    if request.type == "story":
        prompt_template = "Create an engaging story about {query}"
    elif request.type == "podcast":
        prompt_template = "Create an informative podcast script about {query}"
    elif request.type == "sermon":
        prompt_template = "Create an inspiring sermon about {query}"
    elif request.type == "science":
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
            "type": request.type,
            "query": request.query,
            "created_at": datetime.now().isoformat(),
        },
    )


async def get_audiocast(uuid: str):
    # TODO: Implement audiocast retrieval
    pass
