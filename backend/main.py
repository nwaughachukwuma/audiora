import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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


class ChatMessage(BaseModel):
    role: str
    content: str


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
chat_sessions = {}


@app.post("/api/chat/{session_id}")
async def chat(session_id: str, message: ChatMessage):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    chat_sessions[session_id].append(message)

    # Process the message and generate AI response
    # TODO: Implement AI chat logic here
    ai_response = ChatMessage(
        role="assistant",
        content="I understand you're looking for [type] content. Could you provide more specific details about what you'd like to hear?",
    )

    chat_sessions[session_id].append(ai_response)
    return ai_response


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
