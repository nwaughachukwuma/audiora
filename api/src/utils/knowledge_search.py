import asyncio
from dataclasses import dataclass
from typing import List

import httpx
import wikipedia
from bs4 import BeautifulSoup


@dataclass
class KnowledgeSearchModel:
    url: str
    title: str
    content: str


class KnowledgeSearch:
    session: httpx.AsyncClient

    async def fetch_knowledge(self, query: str, max_sources: int = 10):
        """
        Fetch knowledge from multiple sources concurrently,
        including Wikipedia, arXiv, and other scientific sources
        """
        self.session = httpx.AsyncClient(timeout=30.0)
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
            elif isinstance(result, KnowledgeSearchModel):
                sources.append(result)

        # return sources[:max_sources]
        contents: List[str] = []
        for source in sources[:max_sources]:
            if isinstance(source, KnowledgeSearchModel):
                contents.append(f"Title: {source.title}\nPreview: {source.content}")

        await self.session.aclose()
        return "\n\n".join(contents)

    async def search_wikipedia(self, query: str) -> List[KnowledgeSearchModel]:
        """
        Fetch relevant Wikipedia articles
        """
        try:
            search_results = wikipedia.search(query, results=3)
            sources = []

            for title in search_results:
                try:
                    page = wikipedia.page(title)
                    if not page.content:
                        continue

                    content = self._extract_relevant_wiki_sections(page.content)
                    if not content:
                        continue

                    sources.append(KnowledgeSearchModel(title=page.title, content=content, url=page.url))
                except wikipedia.exceptions.DisambiguationError:
                    continue
                except wikipedia.exceptions.PageError:
                    continue

            return sources
        except Exception:
            return []

    async def search_arxiv_papers(self, query: str) -> List[KnowledgeSearchModel]:
        """
        Fetch papers from arXiv and other scientific sources
        """
        ARXIV_URL = "http://export.arxiv.org/api/query"
        try:
            params = {
                "search_query": f"all:{query}",
                "start": 0,
                "max_results": 3,
                "sortBy": "relevance",
                "sortOrder": "descending",
            }

            response = await self.session.get(ARXIV_URL, params=params)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml-xml")
            entries = soup.find_all("entry")

            sources = []
            for entry in entries:
                title = entry.title.text.strip()
                url = entry.id.text.strip()
                abstract = entry.summary.text.strip()

                if abstract:
                    sources.append(KnowledgeSearchModel(title=title, content=abstract, url=url))

            return sources
        except Exception:
            return []

    def _extract_relevant_wiki_sections(self, content: str, max_chars: int = 1024) -> str:
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
            if len(result + p) <= max_chars:
                result += p + "\n\n"
            else:
                break

        return result.strip()
