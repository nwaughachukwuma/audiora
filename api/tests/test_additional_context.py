import asyncio

from web_search import WebSearch

from src.utils.audiocast_request import GenerateSourceContent
from src.utils.audiocast_source_context import SourceContext
from src.utils.chat_utils import ContentCategory
from src.utils.decorators import process_time


async def test_additional_context(preference_summary: str):
    result = await SourceContext().get_context(preference_summary)
    return result


@process_time()
async def test_web_search(query: str):
    web_search = WebSearch()
    return await web_search.search(query)


async def test_generate_source_content(category: ContentCategory, preference_summary: str):
    source_content_generator = GenerateSourceContent(category, preference_summary)
    source_content = await source_content_generator._run()
    return source_content


if __name__ == "__main__":
    query = "What is neuroscience?"
    preference_summary = "You want to listen to a 10-minute audiocast summarizing cutting-edge technologies in modern neuroscience and their real-world applications."
    # ===========================================================================
    result = asyncio.run(test_web_search(query))
    # ===========================================================================
    # result = asyncio.run(test_additional_context(preference_summary))
    # ===========================================================================
    # result = asyncio.run(test_generate_source_content("interview", preference_summary))
    # ===========================================================================
    print(f"Result: {result}")
