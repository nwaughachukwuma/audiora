import asyncio

from api.src.utils.audiocast_source_context import SourceContext

from src.utils.google_search import GoogleSearch


async def test_additional_context(preference_summary: str):
    result = await SourceContext().get_context(preference_summary)
    return result


async def test_google_search(query: str):
    result = await GoogleSearch()._google_search(query)
    return result


if __name__ == "__main__":
    preference_summary = "You want to listen to a 10-minute audiocast summarizing cutting-edge technologies in modern neuroscience and their real-world applications."
    result = asyncio.run(test_additional_context(preference_summary))
    # query = "What is neuroscience?"
    # result = asyncio.run(test_google_search(query))

    print(f"Additional context: {result}")
