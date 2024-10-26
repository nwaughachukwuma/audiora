import uuid
from datetime import datetime
from typing import Dict, List, Optional

from chat_utils import ChatMessage, SessionChatRequest
from chat_with_user import chat_with_user
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from slugify import slugify

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/api/chat/{session_id}")
async def chat(session_id: str, request: SessionChatRequest):
    message = request.message
    content_type = request.content_type

    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    chat_sessions[session_id].append(message)

    async def on_finish(text: str):
        print(f"Chat finished. Text: {text}")
        chat_sessions[session_id].append(ChatMessage(role="assistant", content=text))

    generator = await chat_with_user(
        content_type=content_type,
        previous_messages=chat_sessions[session_id],
        on_finish=on_finish,
    )

    return StreamingResponse(generator, media_type="text/event-stream")


@app.post("/api/generate-audiocast")
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


@app.get("/api/audiocast/{uuid}")
async def get_audiocast(uuid: str):
    # TODO: Implement audiocast retrieval
    pass
