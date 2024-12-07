from io import BytesIO
from time import time
from typing import Any, Callable, Generator

from fastapi import BackgroundTasks, FastAPI, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi_utilities import add_timer_middleware

from .services.storage import BLOB_BASE_URI, StorageManager, UploadItemParams
from .utils.chat_request import chat_request
from .utils.chat_utils import (
    ContentCategory,
    SessionChatItem,
    SessionChatRequest,
)
from .utils.custom_sources.base_utils import SourceContent
from .utils.custom_sources.extract_url_content import ExtractURLContent, ExtractURLContentRequest
from .utils.custom_sources.generate_url_source import (
    CustomSourceManager,
    CustomSourceModel,
    DeleteCustomSourcesRequest,
    GenerateCustomSourceRequest,
    GetCustomSourcesRequest,
    generate_custom_source,
)
from .utils.custom_sources.manage_attachments import ManageAttachments
from .utils.custom_sources.read_content import ReadContent
from .utils.custom_sources.save_copied_source import CopiedPasteSourceRequest, save_copied_source
from .utils.custom_sources.save_uploaded_sources import UploadedFiles
from .utils.decorators.retry_decorator import RetryConfig, retry
from .utils.detect_content_category import DetectContentCategoryRequest, detect_content_category
from .utils.generate_audiocast import GenerateAudioCastRequest, GenerateAudiocastException, generate_audiocast
from .utils.generate_audiocast_source import GenerateAiSourceRequest, generate_ai_source
from .utils.get_audiocast import get_audiocast
from .utils.get_session_title import GetSessionTitleModel, get_session_title
from .utils.session_manager import SessionManager, SessionModel
from .utils.summarize_custom_sources import SummarizeCustomSourcesRequest, summarize_custom_sources

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
async def chat_endpoint(
    session_id: str,
    request: SessionChatRequest,
    background_tasks: BackgroundTasks,
):
    """Chat endpoint"""
    category = request.contentCategory
    attachments = request.attachments

    db = SessionManager(session_id, category)
    db._add_chat(request.chatItem)

    attachment_manager = ManageAttachments(session_id)
    sources_summary = await attachment_manager.get_attachments_summary(db, attachments)

    def on_finish(text: str):
        background_tasks.add_task(db._update, {"status": "collating"})
        background_tasks.add_task(
            db._add_chat,
            SessionChatItem(role="assistant", content=text),
        )

        if attachments:
            background_tasks.add_task(attachment_manager.store_attachments, attachments)

    response = chat_request(
        content_category=category,
        previous_messages=db._get_chats(),
        reference_material=sources_summary,
        on_finish=on_finish,
    )

    return StreamingResponse(response, media_type="text/event-stream")


@app.exception_handler(GenerateAudiocastException)
async def generate_audiocast_exception_handler(_, exc):
    SessionManager._update_status(exc.session_id, "failed")
    return HTTPException(status_code=exc.status_code, detail=str(exc.detail))


@app.post("/audiocast/generate", response_model=str)
async def generate_audiocast_endpoint(
    request: GenerateAudioCastRequest,
    background_tasks: BackgroundTasks,
):
    return await generate_audiocast(request, background_tasks)


@app.get("/audiocast/{session_id}", response_model=SessionModel)
def get_audiocast_endpoint(session_id: str):
    result = get_audiocast(session_id)
    return result


@app.post("/generate-aisource", response_model=str)
async def generate_aisource_endpoint(request: GenerateAiSourceRequest):
    source_content = await generate_ai_source(request)
    if not source_content:
        raise HTTPException(status_code=500, detail="Failed to generate aisource content")
    return source_content


@app.get("/get-signed-url", response_model=str)
async def get_signed_url_endpoint(blobname: str):
    """
    Get signed URL for generated audiocast
    """

    @retry(RetryConfig(max_retries=3, delay=5, backoff=1.5))
    def handler() -> str | None:
        return StorageManager().get_signed_url(blobname=blobname)

    url = handler()
    if not url:
        raise HTTPException(status_code=500, detail="Failed to get signed URL")

    return JSONResponse(
        content=url,
        headers={
            "Content-Type": "application/json",
            "Cache-Control": "public, max-age=86390, immutable",
        },
    )


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


@app.delete("/delete-session/{sessionId}")
def delete_session_endpoint(sessionId: str):
    """
    Delete audiocast session
    """
    SessionManager._delete_session(sessionId)
    return "Deleted"


@app.post("/detect-category", response_model=ContentCategory)
async def detect_category_endpoint(request: DetectContentCategoryRequest):
    """
    Detect category of a given content
    """
    return await detect_content_category(request.content)


@app.post("/store-file-upload", response_model=str)
async def store_file_upload(file: UploadFile, filename: str = Form(...), preserve: bool = Form(False)):
    """
    Store file uploaded from the frontend
    """
    print(f"Storing file: {filename}. Preserve: {preserve}")

    storage_manager = StorageManager()
    file_exists = storage_manager.check_blob_exists(filename)
    if file_exists:
        return storage_manager.get_gcs_url(filename)

    file_content = await ReadContent()._read_file(file, preserve=preserve)
    content_type = (
        file.content_type or "application/octet-stream"
        if preserve or isinstance(file_content, BytesIO)
        else "text/plain"
    )

    result = storage_manager.upload_to_gcs(
        item=file_content,
        blobname=f"{BLOB_BASE_URI}/{filename}",
        params=UploadItemParams(
            cache_control="public, max-age=31536000",
            content_type=content_type,
        ),
    )

    return result


@app.post("/summarize-custom-sources", response_model=str)
async def summarize_custom_sources_endpoint(request: SummarizeCustomSourcesRequest):
    """
    Summarize custom sources from specified source URLs
    """
    return await summarize_custom_sources(request.sourceURLs)
