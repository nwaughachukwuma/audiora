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


def generate_custom_source(request: GenerateCustomSourceRequest, background_tasks: BackgroundTasks):
    extractor = ExtractURLContent()
    page_content = extractor._extract(request.url)

    def save_to_firestore():
        custom_source = CustomSourceModel(
            **page_content.model_dump(),
            url=request.url,
            source_type="link",
        )
        manager = CustomSourceManager(request.sessionId)
        manager._set_custom_source(custom_source)

    background_tasks.add_task(save_to_firestore)
    return page_content.model_dump()
