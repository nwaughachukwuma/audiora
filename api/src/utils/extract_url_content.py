import re
from io import BytesIO
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel
from pypdf import PdfReader

from src.utils.decorators import process_time


class ExtractURLContentRequest(BaseModel):
    url: str


class URLContent(BaseModel):
    content: str
    content_type: str
    metadata: dict = {}

    def __str__(self):
        return f"Content: {self.content}"


class ExtractURLContent:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=self.timeout)

    async def __aenter__(self):
        return self

    async def __exit__(self):
        await self.client.aclose()

    async def __aexit__(self):
        return await self.__exit__()

    def _clean_text(self, text: str) -> str:
        """replace all whitespace sequences with a single space"""
        return re.compile(r"\s+").sub(" ", text).strip()

    async def _extract_pdf(self, content: bytes) -> tuple[str, dict]:
        pdf_reader = PdfReader(BytesIO(content))
        text_content = " ".join(page.extract_text() for page in pdf_reader.pages)
        metadata = {"pages": len(pdf_reader.pages), "info": pdf_reader.metadata or {}}

        return self._clean_text(text_content), metadata

    async def _extract_html(self, content: bytes) -> tuple[str, dict]:
        soup = BeautifulSoup(content, "lxml")
        for element in soup(["script", "style", "nav", "footer"]):
            element.decompose()

        text_content = soup.get_text(separator=" ", strip=True)
        descr_tag = soup.find("meta", {"name": "description"})
        metadata = {
            "title": soup.title.string if soup.title else "",
            "description": descr_tag.get("content") if isinstance(descr_tag, Tag) else "",
        }

        return self._clean_text(text_content), metadata

    @process_time()
    async def _extract(self, url: str) -> URLContent:
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL provided")

        try:
            response = await self.client.get(url)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "").lower()

            if url.lower().endswith(".pdf") or "application/pdf" in content_type:
                text, metadata = await self._extract_pdf(response.content)
                content_type = "application/pdf"
            else:
                text, metadata = await self._extract_html(response.content)
                content_type = "text/html"

            return URLContent(
                content=text,
                content_type=content_type,
                metadata=metadata,
            )
        except Exception as e:
            raise Exception(f"Failed to extract content: {str(e)}")
