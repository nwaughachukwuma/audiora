from io import BytesIO

from fastapi import UploadFile
from pypdf import PdfReader
from docx import Document


class ReadContent:
    def _read_pdf(self, content: bytes) -> tuple[str, PdfReader]:
        pdf_reader = PdfReader(BytesIO(content))

        pages: list[str] = []
        for page in pdf_reader.pages:
            text = page.extract_text()
            # Split into paragraphs and clean
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            pages.append("\n\n".join(paragraphs))

        text_content = "\n\n".join(pages).strip()
        return text_content, pdf_reader

    def _read_txt(self, content: bytes) -> str:
        return content.decode()

    def _read_docx(self, content: bytes) -> str:
        doc = Document(BytesIO(content))
        return "\n\n".join([p.text for p in doc.paragraphs])

    async def _read_file(self, file: UploadFile, preserve: bool):
        file_bytes = await file.read()

        if preserve:
            return BytesIO(file_bytes)

        if file.content_type == "application/pdf":
            text_content, _ = self._read_pdf(file_bytes)
        elif file.content_type == "text/plain":
            text_content = self._read_txt(file_bytes)
        else:
            return BytesIO(file_bytes)

        return text_content
