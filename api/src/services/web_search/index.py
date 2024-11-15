import asyncio

from src.services.web_search.google_search import GoogleSearch
from src.services.web_search.knowledge_search import KnowledgeSearch, __Config


class WebSearch(GoogleSearch, KnowledgeSearch):
    def __init__(self, config: __Config | None = None):
        super().__init__(config=config)

    async def _web_search(self, query: str):
        """
        Search the web for relevant content
        """
        tasks = [
            self._google_search(query),
            self.fetch_knowledge(query),
        ]
        results = await asyncio.gather(*tasks)
        return "\n".join(results)
