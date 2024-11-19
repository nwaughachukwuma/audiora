import re

from src.services.openai_client import get_openai
from src.utils.audiocast_source_context import SourceContext
from src.utils.audiocast_source_refiner import SourceContentRefiner
from src.utils.chat_utils import ContentCategory
from src.utils.prompt_templates.source_content_prompt import generate_source_content_prompt


class GenerateSourceContent(SourceContext, SourceContentRefiner):
    def __init__(self, category: ContentCategory, preference_summary: str):
        SourceContext.__init__(self)
        SourceContentRefiner.__init__(self, category, preference_summary)

    async def _run(self):
        """
        Generate audiocast source conntent based a user preference.
        Args:
            category (ContentCategory): The content category
            preference_summary (str): summary of user preferences
        Returns:
            str: The audiocast source content
        """
        source_content = await self.__use_openai(self.category, self.preference_summary)
        if not source_content:
            raise ValueError("Failed to generate audiocast source content")

        return self._refine(source_content)

    async def __use_openai(self, category: ContentCategory, preference_summary: str):
        """
        Generate audiocast source content using OpenAI.
        """
        refined_summary = re.sub("You want", "A user who wants", preference_summary, flags=re.IGNORECASE)
        refined_summary = re.sub("You", "A user", refined_summary, flags=re.IGNORECASE)

        additional_context = await self.get_context(self.preference_summary)
        print(f">>> Additional context: {additional_context}")

        response = get_openai().chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": generate_source_content_prompt(
                        category,
                        refined_summary,
                        additional_context,
                    ),
                },
                {
                    "role": "user",
                    "content": "Now comprehensively and exhaustively develop the content.",
                },
            ],
            temperature=0.3,
            max_tokens=8048,
        )

        return response.choices[0].message.content
