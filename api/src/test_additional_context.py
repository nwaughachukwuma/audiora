import asyncio

from src.utils.audiocast_request import GenerateSourceContent
from src.utils.audiocast_source_context import SourceContext
from src.utils.chat_utils import ContentCategory
from src.utils.google_search import GoogleSearch


async def test_additional_context(preference_summary: str):
    result = await SourceContext().get_context(preference_summary)
    return result


async def test_google_search(query: str):
    result = await GoogleSearch()._google_search(query)
    return result


async def test_generate_source_content(category: ContentCategory, preference_summary: str):
    source_content_generator = GenerateSourceContent(category, preference_summary)
    source_content = await source_content_generator._run()
    return source_content


if __name__ == "__main__":
    preference_summary = "You want to listen to a 10-minute audiocast summarizing cutting-edge technologies in modern neuroscience and their real-world applications."
    # result = asyncio.run(test_additional_context(preference_summary))
    # ===========================================================================
    # query = "What is neuroscience?"
    # result = asyncio.run(test_google_search(query))
    # ===========================================================================
    result = asyncio.run(test_generate_source_content("interview", preference_summary))
    print(f"Source Context: {result}")
