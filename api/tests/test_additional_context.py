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
    return await WebSearch().search(query)


async def test_generate_source_content(category: ContentCategory, preference_summary: str):
    source_content_generator = GenerateSourceContent(category, preference_summary)
    return await source_content_generator._run()


if __name__ == "__main__":
    query = "What is neuroscience?"
    preference_summary = "You want to listen to an audiocast that provides an overview of the history of blockchain, covering its origin, key milestones, and recent developments."
    # ===========================================================================
    # result = asyncio.run(test_web_search(query))
    # ===========================================================================
    # result = asyncio.run(test_additional_context(preference_summary))
    # ===========================================================================
    result = asyncio.run(test_generate_source_content("interview", preference_summary))
    # ===========================================================================
    print(f"Result: {result}")
