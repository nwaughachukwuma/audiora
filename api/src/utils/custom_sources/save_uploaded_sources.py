from uuid import uuid4

from fastapi import UploadFile
from pydantic import BaseModel

from .base_utils import CustomSourceManager, CustomSourceModel
from .extract_url_content import URLContent
from .read_content import ReadContent


class UploadedSourcesRequest(BaseModel):
    sessionId: str
    files: list[UploadFile]


class UploadedContent(URLContent):
    pass


class UploadContent:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.content_reader = ReadContent()

    async def _extract_content(self, file: UploadFile):
        file_bytes = await file.read()

        print(f"FILE_INFO>>>: {file.filename}, Size: {len(file_bytes)} bytes")

        if file.content_type == "application/pdf":
            text_content, metadata = self.__pdf_content(file_bytes)
            content_type = "application/pdf"
        else:
            text_content, metadata = self.content_reader._read_txt(file_bytes), {}
            content_type = "text/plain"

        return UploadedContent(
            id=str(uuid4()),
            content=text_content,
            content_type=content_type,
            metadata=metadata,
        )

    def __pdf_content(self, content: bytes) -> tuple[str, dict]:
        text_content, pdf_reader = self.content_reader._read_pdf(content)
        metadata = {**(pdf_reader.metadata or {}), "pages": pdf_reader.get_num_pages()}

        return text_content, metadata

    async def _save_uploaded_sources(self, request: UploadedSourcesRequest):
        contents = [self._extract_content(file) for file in request.files]

        manager = CustomSourceManager(request.sessionId)
        for content in contents:
            _content = await content
            custom_source = CustomSourceModel(
                **_content.model_dump(),
                source_type="file_upload",
            )
            manager._set_custom_source(custom_source)

        return "Saved"
