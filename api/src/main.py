from time import time
from typing import Any, Callable, Generator

from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utilities import add_timer_middleware

from src.utils.chat_request import chat_request
from src.utils.generate_audiocast import (
    GenerateAudioCastRequest,
    GenerateAudioCastResponse,
    generate_audiocast,
)
from src.utils.get_audiocast import get_audiocast
from shared_utils_pkg.chat_utils import (
    SessionChatMessage,
    SessionChatRequest,
)
from shared_utils_pkg.session_manager import SessionManager

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
async def chat_endpoint(session_id: str, request: SessionChatRequest, background_tasks: BackgroundTasks):
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
    result = await generate_audiocast(request, background_tasks)
    return result


@app.get("/audiocast/{session_id}", response_model=GenerateAudioCastResponse)
async def get_audiocast_endpoint(session_id: str):
    result = get_audiocast(session_id)
    return result
