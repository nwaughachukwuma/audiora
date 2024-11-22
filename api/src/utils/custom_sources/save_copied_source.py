from uuid import uuid4

from pydantic import BaseModel

from .generate_custom_source import CustomSourceManager, CustomSourceModel


class CopiedPasteSourceRequest(BaseModel):
    sessionId: str
    text: str


def save_copied_source(request: CopiedPasteSourceRequest):
    custom_source = CustomSourceModel(
        id=str(uuid4()),
        content=request.text,
        content_type="text/plain",
        source_type="copy/paste",
    )

    CustomSourceManager(request.sessionId)._set_custom_source(custom_source)
    return "Saved"
