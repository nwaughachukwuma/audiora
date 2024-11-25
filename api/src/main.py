import asyncio
from time import time
from typing import Any, Callable, Generator

from fastapi import BackgroundTasks, FastAPI, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi_utilities import add_timer_middleware

from src.services.storage import StorageManager
from src.utils.chat_request import chat_request
from src.utils.chat_utils import (
    SessionChatItem,
    SessionChatRequest,
)
from src.utils.custom_sources.base_utils import SourceContent
from src.utils.custom_sources.extract_url_content import ExtractURLContent, ExtractURLContentRequest
from src.utils.custom_sources.generate_url_source import (
    CustomSourceManager,
    CustomSourceModel,
    DeleteCustomSourcesRequest,
    GenerateCustomSourceRequest,
    GetCustomSourcesRequest,
    generate_custom_source,
)
from src.utils.custom_sources.save_copied_source import CopiedPasteSourceRequest, save_copied_source
from src.utils.custom_sources.save_uploaded_sources import UploadedFiles
from src.utils.generate_audiocast import (
    GenerateAudioCastRequest,
    GenerateAudioCastResponse,
    generate_audiocast,
)
from src.utils.generate_audiocast_source import GenerateAudiocastSource, generate_audiocast_source
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
def root():
    return {"message": "Hello World"}


@app.post("/chat/{session_id}", response_model=Generator[str, Any, None])
def chat_endpoint(
    session_id: str,
    request: SessionChatRequest,
    background_tasks: BackgroundTasks,
):
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
def get_audiocast_endpoint(session_id: str):
    result = get_audiocast(session_id)
    return result


@app.post("/generate-audiocast-source", response_model=str)
async def generate_audiocast_source_endpoint(request: GenerateAudiocastSource):
    source_content = await generate_audiocast_source(request)
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
async def get_session_title_endpoint(
    request: GetSessionTitleModel,
    background_tasks: BackgroundTasks,
):
    return await get_session_title(request, background_tasks)


@app.post("/extract-url-content", response_model=SourceContent)
def extract_url_content_endpoint(request: ExtractURLContentRequest):
    extractor = ExtractURLContent()
    page_content = extractor._extract(request.url)
    return page_content.model_dump()


@app.post("/generate-url-source", response_model=SourceContent)
def generate_url_source_endpoint(
    request: GenerateCustomSourceRequest,
    background_tasks: BackgroundTasks,
):
    return generate_custom_source(request, background_tasks)


@app.post("/get-custom-sources", response_model=list[CustomSourceModel])
async def get_custom_sources_endpoint(request: GetCustomSourcesRequest):
    return CustomSourceManager(request.sessionId)._get_custom_sources()


@app.post("/delete-custom-source", response_model=list[CustomSourceModel])
def delete_custom_source_endpoint(request: DeleteCustomSourcesRequest):
    manager = CustomSourceManager(request.sessionId)
    manager._delete_custom_source(request.sourceId)
    return "Deleted"


@app.post("/save-copied-source", response_model=str)
def save_copied_source_endpoint(request: CopiedPasteSourceRequest):
    result = save_copied_source(request)
    return result


@app.post("/save-uploaded-sources", response_model=str)
async def save_uploaded_files_endpoint(files: list[UploadFile], sessionId: str = Form(...)):
    """
    Save sources uploaded from the frontend
    """
    result = await UploadedFiles(session_id=sessionId)._save_sources(files)
    return result
