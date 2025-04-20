import asyncio

from pydantic import BaseModel

from src.services.gemini_client import get_gemini
from src.services.storage import StorageManager

from .custom_sources.read_content import ReadContent
from .decorators.base import process_time


class SummarizeCustomSourcesRequest(BaseModel):
    sourceURLs: list[str]


def summarize_custom_sources_prompt(combined_content: str) -> str:
    """
    Summarize a list of custom sources using Gemini Flash.
    """
    return f"""Please provide a comprehensive 3-paragraph summary of the following content.
    Each paragraph should serve a specific purpose:

    Paragraph 1: Introduce the main topics and key themes discussed across all sources.
    Paragraph 2: Dive into the most significant details, findings, or arguments presented.
    Paragraph 3: Conclude with the implications, connections between ideas, or final insights.

    Maintain high fidelity to the source material and ensure all critical information is preserved.

    Content to summarize: {combined_content}
    """


async def get_source_content(source_url: str):
    """
    Get the content of a source URL.
    """
    storage_manager = StorageManager()
    content_reader = ReadContent()

    blob_name = source_url.replace(f"gs://{storage_manager.bucket_name}/", "")
    blob = storage_manager.get_blob(blob_name)
    content_byte = blob.download_as_bytes()

    if blob.content_type == "application/pdf":
        text_content, _ = content_reader._read_pdf(content_byte)
    elif blob.content_type == "text/plain":
        text_content = content_reader._read_txt(content_byte)
    elif blob.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text_content = content_reader._read_docx(content_byte)
    else:
        print(f"Unsupported content type: {blob.content_type}")
        return None

    return text_content


async def get_sources_str(source_urls: list[str]) -> str:
    """
    Get the content of a list of source URLs.
    """
    tasks = [get_source_content(source_url) for source_url in source_urls]
    sources = await asyncio.gather(*tasks, return_exceptions=True)

    valid_sources = [source for source in sources if isinstance(source, str)]
    return "\n\n".join(valid_sources)


@process_time()
async def summarize_custom_sources(source_urls: list[str]) -> str:
    """
    Summarize the contents of list of custom sources using Gemini Flash.
    """
    content = await get_sources_str(source_urls)

    client = get_gemini()

    model = client.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=summarize_custom_sources_prompt(content),
        generation_config=client.GenerationConfig(
            temperature=0.1,
            max_output_tokens=2048,
            response_mime_type="text/plain",
        ),
    )

    response = model.generate_content(["Now, provide the summary"])
    if not response.text:
        raise Exception("Error obtaining response from Gemini Flash")

    return response.text
