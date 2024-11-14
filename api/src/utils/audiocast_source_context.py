import asyncio

from src.services.gemini_client import GeminiConfig, generate_content
from src.utils.google_search import GoogleSearch
from src.utils.knowledge_search import KnowledgeSearch
from src.utils.prompt_templates.searchable_queries_prompt import searchable_queries_prompt


class SourceContext(KnowledgeSearch, GoogleSearch):
    def _get_search_queries(self, preference_summary: str):
        """
        Summarize the user preference into searchable phrases/queries
        """
        result = generate_content(
            prompt=[f"Summarize the following preference summary into a searchable phrase/query: {preference_summary}"],
            config=GeminiConfig(
                model_name="gemini-1.5-flash-002",
                system_prompt=searchable_queries_prompt(),
                temperature=0.1,
                max_output_tokens=64,
            ),
        )

        return str(result).strip().split("###")[:3]

    async def get_context(self, preference_summary: str):
        """
        Fetch additional context to augment the source content.
        ## Steps:
        1. summarize the user preference into a searchable phrases/queries
        2. perform a web search to get additional context using the query above, focusing on wikipedia and other relevant data sources
        """
        queries = self._get_search_queries(preference_summary)
        if not queries:
            return ""

        web_tasks = [self._google_search(query) for query in queries]
        knowlege_tasks = [self.fetch_knowledge(query) for query in queries]
        result = await asyncio.gather(*web_tasks, *knowlege_tasks)

        return "\n\n".join(result)
