from urllib.parse import urlparse
from uuid import uuid4

import httpx
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel

from src.services.storage import StorageManager
from src.utils.decorators.base import process_time

from .base_utils import SourceContent
from .read_content import ReadContent


class ExtractURLContentRequest(BaseModel):
    url: str


class ExtractURLContent(ReadContent):
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def _clean_text(self, text: str) -> str:
        """TODO: write text cleaning logic"""
        return text.strip()

    def _extract_pdf(self, content: bytes) -> tuple[str, dict]:
        text_content, pdf_reader = self._read_pdf(content)
        metadata = {**(pdf_reader.metadata or {}), "pages": pdf_reader.get_num_pages()}
        return self._clean_text(text_content), metadata

    def _extract_html(self, content: bytes) -> tuple[str, dict]:
        soup = BeautifulSoup(content, "lxml")
        for element in soup(["script", "style", "nav", "footer"]):
            element.decompose()

        text_content = soup.get_text(separator="\n\n", strip=True)
        descr_tag = soup.find("meta", {"name": "description"})
        metadata = {
            "title": soup.title.string if soup.title else "",
            "description": descr_tag.get("content") if isinstance(descr_tag, Tag) else "",
        }

        return self._clean_text(text_content), metadata

    def _resolve_gcs_url(self, url) -> str:
        if url.startswith("gs://"):
            storage_manager = StorageManager()
            blobame = storage_manager.get_blobname_from_url(url)
            return storage_manager.get_signed_url(blobame)

        return url

    @process_time()
    def _extract(self, url: str) -> SourceContent:
        resolved_url = self._resolve_gcs_url(url)

        parsed_url = urlparse(resolved_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL provided")

        try:
            response = httpx.get(resolved_url)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "").lower()

            if url.lower().endswith(".pdf") or "application/pdf" in content_type:
                text, metadata = self._extract_pdf(response.content)
                content_type = "application/pdf"
            else:
                text, metadata = self._extract_html(response.content)
                content_type = "text/html"

            return SourceContent(
                id=str(uuid4()),
                content=text,
                content_type=content_type,
                metadata=metadata,
            )
        except Exception as e:
            raise Exception(f"Failed to extract content: {str(e)}")
