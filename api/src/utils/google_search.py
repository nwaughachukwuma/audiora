import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List
from urllib.parse import unquote

import httpx
from bs4 import BeautifulSoup

from src.env_var import CSE_API_KEY, CSE_ID

GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"


@dataclass
class SearchResult:
    url: str
    title: str
    preview: str


class GoogleSearch:
    async def _google_search(self, query: str, limit=3, **kwargs):
        """
        Perform a Google search using the Custom Search Engine API
        """
        params = {"q": unquote(query), "key": CSE_API_KEY, "cx": CSE_ID, "num": 5}
        params.update(kwargs)
        headers = {"Referer": "https://veedo.ai"}

        response = httpx.get(GOOGLE_SEARCH_URL, params=params, headers=headers)
        response.raise_for_status()
        json_data = response.json()

        items = json_data.get("items", [])[:limit]
        result = await self.extract_relevant_items(items)

        return result

    async def extract_relevant_items(self, search_results: List[Dict[str, Any]]) -> str:
        """
        Extract relevant items from the search results
        """
        tasks = []
        for item in search_results:
            url = item.get("link", "")
            if url and self._is_valid_url(url):
                tasks.append(self._process_search_item(item))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        contents: List[str] = []
        for item in results:
            if isinstance(item, SearchResult) and item.preview:
                contents.append(f"Title: {item.title}\nPreview: {item.preview}")

        return "\n\n".join(contents)

    async def _process_search_item(self, item: Dict, char_limit=2000) -> SearchResult | None:
        """
        Process a single search result item and fetch its content
        """
        try:
            url = item.get("link", "")
            if not url:
                raise ValueError("No URL found in search item")

            content = await self._scrape_page_content(url)
            return SearchResult(url=url, title=item.get("title", ""), preview=content[:char_limit])
        except Exception:
            return None

    async def _scrape_page_content(self, url: str) -> str:
        """
        Fetch and extract content from a webpage
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")
            # Remove unwanted elements
            for element in soup.find_all(["script", "style", "nav", "header", "footer", "ads"]):
                element.decompose()

            content_elements = soup.find_all(
                ["article", "main", "div"], class_=["content", "article", "post", "entry", "main-content"]
            )

            if not content_elements:
                # Fallback to paragraph extraction if no main content container found
                content_elements = soup.find_all("p")

            # Extract text from found elements
            content = "\n".join(
                element.get_text(strip=True) for element in content_elements if element.get_text(strip=True)
            )

            # If still no content, try getting all text
            if not content:
                content = soup.get_text(strip=True)

            return self._clean_content(content)
        except Exception:
            return ""

    def _clean_content(self, content: str) -> str:
        content = " ".join(content.split())
        # Remove very short lines (likely navigation/menu items)
        lines = [line for line in content.split("\n") if len(line) > 30]
        return "\n".join(lines)

    def _is_valid_url(self, url: str) -> bool:
        invalid_extensions = (".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".zip", ".rar")
        invalid_domains = ("youtube.com", "vimeo.com", "facebook.com", "twitter.com")
        return not (url.endswith(invalid_extensions) or any(domain in url for domain in invalid_domains))
