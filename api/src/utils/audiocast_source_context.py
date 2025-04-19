import asyncio

from web_search import WebSearch

from src.services.gemini_client import GeminiConfig, generate_content
from src.utils.prompt_templates.searchable_queries_prompt import searchable_queries_prompt


class SourceContext(WebSearch):
    def __init__(self):
        super().__init__()

    def _get_search_queries(self, preference_summary: str):
        """
        Summarize the user preference into searchable phrases/queries
        """
        result = generate_content(
            prompt=[f"Summarize the following preference summary into a searchable phrase/query: {preference_summary}"],
            config=GeminiConfig(
                model_name="gemini-2.0-flash",
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

        tasks = [self.search(query) for query in queries]
        result = await asyncio.gather(*tasks)
        return "\n\n".join(result)
