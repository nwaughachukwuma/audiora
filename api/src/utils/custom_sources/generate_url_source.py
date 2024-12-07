from fastapi import BackgroundTasks
from pydantic import BaseModel

from src.utils.custom_sources.extract_url_content import ExtractURLContent

from .base_utils import CustomSourceManager, CustomSourceModel


class GenerateCustomSourceRequest(BaseModel):
    url: str
    sessionId: str


class GetCustomSourcesRequest(BaseModel):
    sessionId: str


class DeleteCustomSourcesRequest(BaseModel):
    sessionId: str
    sourceId: str


def generate_custom_source(
    request: GenerateCustomSourceRequest,
    background_tasks: BackgroundTasks | None = None,
):
    extractor = ExtractURLContent()
    content = extractor._extract(request.url)

    def save_to_firestore():
        custom_source = CustomSourceModel(
            **content.model_dump(),
            url=request.url,
            source_type="link",
        )
        manager = CustomSourceManager(request.sessionId)
        manager._set_custom_source(custom_source)

    if background_tasks:
        background_tasks.add_task(save_to_firestore)
    else:
        save_to_firestore()

    return content.model_dump()
