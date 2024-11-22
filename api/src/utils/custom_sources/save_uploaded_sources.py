from uuid import uuid4

from fastapi import UploadFile

from .base_utils import CustomSourceManager, CustomSourceModel, SourceContent
from .read_content import ReadContent

FIVE_MB = 5 * 1024 * 1024


class UploadedFiles:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.content_reader = ReadContent()

    async def _extract_content(self, file: UploadFile):
        file_bytes = await file.read()
        print(f"FILE_INFO>>>: {file.filename}, Size: {len(file_bytes)} bytes")

        # ensure file size is less than 5MB
        if len(file_bytes) > FIVE_MB:
            return None

        if file.content_type == "application/pdf":
            text_content, pdf_reader = self.content_reader._read_pdf(file_bytes)

            metadata = {**(pdf_reader.metadata or {}), "pages": pdf_reader.get_num_pages()}
            content_type = "application/pdf"
        elif file.content_type == "text/plain":
            text_content = self.content_reader._read_txt(file_bytes)

            metadata = {}
            content_type = "text/plain"
        else:
            return None

        return SourceContent(
            id=str(uuid4()),
            content=text_content,
            content_type=content_type,
            metadata=metadata,
        )

    async def _save_sources(self, files: list[UploadFile]):
        manager = CustomSourceManager(self.session_id)

        for file in files:
            content = await self._extract_content(file)
            if content:
                custom_source = CustomSourceModel(**content.model_dump(), source_type="file_upload")
                manager._set_custom_source(custom_source)

        return "Saved"
