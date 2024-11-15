import asyncio
from dataclasses import dataclass

import httpx
import wikipedia
from bs4 import BeautifulSoup


@dataclass
class KnowledgeSearchConfig:
    max_results: int = 3
    max_sources: int = 10
    max_preview_chars: int = 1024


@dataclass
class SearchResult:
    url: str
    title: str
    preview: str

    def __str__(self):
        return f"Title: {self.title}\nPreview: {self.preview}"


class KnowledgeSearch:
    config: KnowledgeSearchConfig

    def __init__(self, config: KnowledgeSearchConfig | None = None):
        self.config = config if config else KnowledgeSearchConfig()

    async def fetch_knowledge(self, query: str):
        """
        Fetch knowledge from multiple sources concurrently,
        including Wikipedia, arXiv, and other scientific sources
        """
        # listed in order of importance
        tasks = [
            self._search_wikipedia(query),
            self._search_arxiv_papers(query),
            # add more knowledge sources here
        ]

        sources: list[SearchResult] = []

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, list):
                sources.extend(result)

        sources = sources[: self.config.max_sources]
        return "\n\n".join(str(source) for source in sources if source.preview)

    async def _compile_wikipedia(self, query: str) -> str:
        results = await self._search_wikipedia(query)
        return "\n\n".join(str(item) for item in results)

    async def _compile_arxiv_papers(self, query: str) -> str:
        results = await self._search_arxiv_papers(query)
        return "\n\n".join(str(item) for item in results)

    async def _search_wikipedia(self, query: str) -> list[SearchResult]:
        """
        Fetch relevant Wikipedia articles
        """
        try:
            sources: list[SearchResult] = []
            search_results = wikipedia.search(query, results=self.config.max_results)

            for title in search_results:
                try:
                    page = wikipedia.page(title)
                    if not page.content:
                        continue

                    preview = self._extract_relevant_wiki_sections(page.content)
                    if not preview:
                        continue

                    sources.append(SearchResult(url=page.url, title=page.title, preview=preview))
                except wikipedia.exceptions.DisambiguationError:
                    continue
                except wikipedia.exceptions.PageError:
                    continue

            return sources
        except Exception:
            return []

    async def _search_arxiv_papers(self, query: str) -> list[SearchResult]:
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

            sources: list[SearchResult] = []
            for entry in entries:
                title = entry.title.text.strip()
                url = entry.id.text.strip()
                preview = entry.summary.text.strip()

                if not preview:
                    continue

                sources.append(SearchResult(url=url, title=title, preview=preview))

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
            if len(result + p) <= self.config.max_preview_chars:
                result += p + "\n\n"
            else:
                break

        return result.strip()
