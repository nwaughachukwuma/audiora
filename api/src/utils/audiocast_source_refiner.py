from src.services.gemini_client import GeminiConfig, generate_content
from src.utils.chat_utils import ContentCategory
from src.utils.prompt_templates.source_refiner_prompt import get_source_refiner_prompt


class SourceContentRefiner:
    category: ContentCategory

    def __init__(self, category: ContentCategory, preference_summary: str):
        self.category = category
        self.preference_summary = preference_summary

    def _refine(self, content: str):
        """
        Moderate and augment the source content to ensure it aligns with the user's preferences.
        """
        return self.__use_gemini_flash(content)

    def __use_gemini_flash(self, content: str):
        response = generate_content(
            prompt=["Now refine the content to match the user's preferences."],
            config=GeminiConfig(
                model_name="gemini-1.5-flash-002",
                system_prompt=get_source_refiner_prompt(content, self.category, self.preference_summary),
                temperature=0.1,
                max_output_tokens=8048,
            ),
        )

        return str(response)
