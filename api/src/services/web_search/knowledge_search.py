import asyncio
from dataclasses import dataclass
from typing import List

import httpx
import wikipedia
from bs4 import BeautifulSoup


@dataclass
class __Config:
    max_results: int = 3
    max_sources: int = 10
    preview_max_chars: int = 1024


@dataclass
class SearchResult:
    url: str
    title: str
    content: str


class KnowledgeSearch:
    config: __Config

    def __init__(self, config: __Config | None = None):
        self.config = config if config else __Config()

    async def fetch_knowledge(self, query: str):
        """
        Fetch knowledge from multiple sources concurrently,
        including Wikipedia, arXiv, and other scientific sources
        """
        # listed in order of importance
        tasks = [
            self.search_wikipedia(query),
            self.search_arxiv_papers(query),
            # add more knowledge sources here
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        sources = []
        for result in results:
            if isinstance(result, Exception):
                continue
            if isinstance(result, list):
                sources.extend(result)
            elif isinstance(result, SearchResult):
                sources.append(result)

        contents: List[str] = []
        for source in sources[: self.config.max_sources]:
            if isinstance(source, SearchResult):
                contents.append(f"Title: {source.title}\nPreview: {source.content}")

        return "\n\n".join(contents)

    async def search_wikipedia(self, query: str) -> List[SearchResult]:
        """
        Fetch relevant Wikipedia articles
        """
        sources = []
        try:
            search_results = wikipedia.search(query, results=self.config.max_results)

            for title in search_results:
                try:
                    page = wikipedia.page(title)
                    if not page.content:
                        continue

                    content = self._extract_relevant_wiki_sections(page.content)
                    if not content:
                        continue

                    sources.append(SearchResult(url=page.url, title=page.title, content=content))
                except wikipedia.exceptions.DisambiguationError:
                    continue
                except wikipedia.exceptions.PageError:
                    continue

            return sources
        except Exception:
            return []

    async def search_arxiv_papers(self, query: str) -> List[SearchResult]:
        """
        Fetch papers from arXiv and other scientific sources
        """
        ARXIV_URL = "http://export.arxiv.org/api/query"
        try:
            params = {
                "search_query": f"all:{query}",
                "start": 0,
                "max_results": self.config.max_results,
                "sortBy": "relevance",
                "sortOrder": "descending",
            }
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.get(ARXIV_URL, params=params)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml-xml")
            entries = soup.find_all("entry")

            sources = []
            for entry in entries:
                title = entry.title.text.strip()
                url = entry.id.text.strip()
                abstract = entry.summary.text.strip()

                if abstract:
                    sources.append(SearchResult(url=url, title=title, content=abstract))

            return sources
        except Exception:
            return []

    def _extract_relevant_wiki_sections(self, content: str) -> str:
        """
        Extract the most relevant sections from Wikipedia content
        """
        paragraphs = content.split("\n\n")
        # Remove references and other metadata
        cleaned_paragraphs = [
            p
            for p in paragraphs
            if not any(marker in p.lower() for marker in ["references", "external links", "see also", "== notes =="])
        ]

        result = ""
        for p in cleaned_paragraphs:
            if len(result + p) <= self.config.preview_max_chars:
                result += p + "\n\n"
            else:
                break

        return result.strip()
