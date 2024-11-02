from datetime import datetime
from time import time
from typing import Any, Callable, Generator

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utilities import add_timer_middleware

from services.storage import StorageManager
from src.utils.generate_audiocast import (
    GenerateAudioCastRequest,
    GenerateAudioCastResponse,
    generate_audiocast,
)
from utils_pkg.chat_request import chat_request
from utils_pkg.chat_utils import (
    SessionChatMessage,
    SessionChatRequest,
)
from utils_pkg.session_manager import SessionManager

app = FastAPI(title="Audiora", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

add_timer_middleware(app, show_avg=True)


@app.middleware("http")
async def inject_exec_time_header(request: Request, call_next: Callable):
    """add request execution time header"""
    start_time = time()
    response = await call_next(request)
    response.headers["X-Execution-Time"] = f"{(time() - start_time):.2f}s"
    return response


@app.middleware("http")
async def log_request_headers(request: Request, call_next: Callable):
    """log request headers"""
    print("Request headers: %s", request.headers)
    return await call_next(request)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/chat/{session_id}", response_model=Generator[str, Any, None])
async def chat_endpoint(
    session_id: str, request: SessionChatRequest, background_tasks: BackgroundTasks
):
    content_category = request.content_category
    db = SessionManager(session_id)
    db._add_chat(request.message)

    def on_finish(text: str):
        background_tasks.add_task(
            db._add_chat,
            SessionChatMessage(role="assistant", content=text),
        )

    response = chat_request(
        content_category=content_category,
        previous_messages=db._get_chats(),
        on_finish=on_finish,
    )

    return response


@app.post("/audiocast/generate", response_model=GenerateAudioCastResponse)
async def generate_audiocast_endpoint(
    request: GenerateAudioCastRequest,
    background_tasks: BackgroundTasks,
):
    return await generate_audiocast(request, background_tasks)


@app.get("/audiocast/{session_id}", response_model=GenerateAudioCastResponse)
async def get_audiocast_endpoint(session_id: str):
    try:
        storage_manager = StorageManager()
        filepath = storage_manager.download_from_gcs(session_id)

        session_data = SessionManager(session_id).data()
        if not session_data:
            raise HTTPException(
                status_code=404,
                detail=f"Audiocast not found for session_id: {session_id}",
            )

        metadata = session_data.metadata
        source = metadata.source if metadata else ""
        transcript = metadata.transcript if metadata else ""

        created_at = None
        if session_data.created_at:
            created_at = datetime.fromisoformat(session_data.created_at).strftime(
                "%Y-%m-%d %H:%M"
            )

        return GenerateAudioCastResponse(
            url=filepath,
            script=transcript,
            source_content=source,
            created_at=created_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
