import asyncio
from time import time
from typing import Any, Callable, Generator

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi_utilities import add_timer_middleware

from src.services.storage import StorageManager
from src.utils.chat_request import chat_request
from src.utils.chat_utils import (
    SessionChatItem,
    SessionChatRequest,
)
from src.utils.extract_url_content import ExtractURLContent, ExtractURLContentRequest, URLContent
from src.utils.generate_audiocast import (
    GenerateAudioCastRequest,
    GenerateAudioCastResponse,
    generate_audiocast,
)
from src.utils.generate_audiocast_source import GenerateAudiocastSource, generate_audiocast_source
from src.utils.generate_custom_source import GenerateCustomSourceRequest, generate_custom_source
from src.utils.get_audiocast import get_audiocast
from src.utils.get_session_title import GetSessionTitleModel, get_session_title
from src.utils.session_manager import SessionManager

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
    """Chat endpoint"""
    category = request.contentCategory
    db = SessionManager(session_id, category)
    db._add_chat(request.chatItem)

    def on_finish(text: str):
        background_tasks.add_task(
            db._add_chat,
            SessionChatItem(role="assistant", content=text),
        )

    response = chat_request(
        content_category=category,
        previous_messages=db._get_chats(),
        on_finish=on_finish,
    )

    return StreamingResponse(response, media_type="text/event-stream")


@app.post("/audiocast/generate", response_model=GenerateAudioCastResponse)
async def generate_audiocast_endpoint(
    request: GenerateAudioCastRequest,
    background_tasks: BackgroundTasks,
):
    return await generate_audiocast(request, background_tasks)


@app.get("/audiocast/{session_id}", response_model=GenerateAudioCastResponse)
async def get_audiocast_endpoint(session_id: str):
    result = get_audiocast(session_id)
    return result


@app.post("/generate-audiocast-source", response_model=str)
async def generate_audiocast_source_endpoint(request: GenerateAudiocastSource, background_tasks: BackgroundTasks):
    source_content = await generate_audiocast_source(request, background_tasks)
    if not source_content:
        raise HTTPException(status_code=500, detail="Failed to generate source content")
    return source_content


@app.get("/get-signed-url", response_model=str)
async def get_signed_url_endpoint(blobname: str):
    """
    Get signed URL for generated audiocast
    """
    retry_count = 0
    max_retries = 3
    errors: list[str] = []

    while retry_count < max_retries:
        try:
            url = StorageManager().get_signed_url(blobname=blobname)
            return JSONResponse(
                content=url,
                headers={
                    "Content-Type": "application/json",
                    "Cache-Control": "public, max-age=86390, immutable",
                },
            )
        except Exception as e:
            errors.append(str(e))

        await asyncio.sleep(5)
        retry_count += 1

    raise HTTPException(status_code=500, detail="".join(errors))


@app.post("/get-session-title", response_model=str)
async def get_session_title_endpoint(request: GetSessionTitleModel, background_tasks: BackgroundTasks):
    return await get_session_title(request, background_tasks)


@app.post("/extract-url-content", response_model=URLContent)
async def extract_url_content_endpoint(request: ExtractURLContentRequest):
    extractor = ExtractURLContent()
    page_content = await extractor._extract(request.url)
    return page_content.model_dump()


@app.post("/generate-custom-source", response_model=URLContent)
async def generate_custom_source_endpoint(request: GenerateCustomSourceRequest, background_tasks: BackgroundTasks):
    return await generate_custom_source(request, background_tasks)
