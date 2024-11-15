import asyncio
from dataclasses import dataclass, field
from typing import Any, Coroutine, List, Literal

from src.services.web_search.google_search import GoogleSearch, GoogleSearchConfig
from src.services.web_search.knowledge_search import KnowledgeSearch, KnowledgeSearchConfig

SearchSources = Literal["google", "wikipedia", "arxiv"]


@dataclass
class WebSearchConfig:
    sources: list[SearchSources] = field(default_factory=lambda: ["google"])
    knowledge_config: KnowledgeSearchConfig | None = None
    google_config: GoogleSearchConfig | None = None


class WebSearch(GoogleSearch, KnowledgeSearch):
    def __init__(self, ws_config: WebSearchConfig | None = None):
        self.ws_config = ws_config if ws_config else WebSearchConfig()
        self.sources = self.ws_config.sources

        GoogleSearch.__init__(self, self.ws_config.google_config)
        KnowledgeSearch.__init__(self, config=self.ws_config.knowledge_config)

    async def _web_search(self, query: str):
        """
        Search the web for relevant content
        """
        tasks: List[Coroutine[Any, Any, str]] = []

        if "google" in self.sources:
            tasks.append(self._compile_google_search(query))
        if "wikipedia" in self.sources:
            tasks.append(self._compile_wikipedia(query))
        if "arxiv" in self.sources:
            tasks.append(self._compile_arxiv_papers(query))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return "\n\n".join(item for item in results if isinstance(item, str))
