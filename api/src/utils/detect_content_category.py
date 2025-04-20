from pydantic import BaseModel

from src.services.gemini_client import get_gemini
from src.utils.chat_utils import ContentCategory, content_categories


class DetectContentCategoryRequest(BaseModel):
    content: str


def detect_category_prompt(content: str) -> str:
    """
    System Prompt to detect the category of a given content
    """
    return f"""You are an intelligent content type classifier. Your task is to analyze the given content and categorize it into one of the following types:
    CONTENT: "{content}"

    CATEGORIES: {", ".join(content_categories)}


    IMPORTANT NOTE:
    - You must ONLY output one of these exact category names, with no additional text, explanation, preamble or formatting.
    - If the content doesn't fit any of the categories, you should output "other".

    Examples:
    Input: "Welcome to today's episode where we'll be discussing the fascinating world of quantum computing..."
    Output: podcast

    Input: "And now, dear brothers and sisters, let us reflect on the profound message in today's scripture..."
    Output: sermon

    Input: "Let's dive into today's lecture on advanced machine learning algorithms..."
    Output: lecture
"""


def validate_category_output(output: str) -> ContentCategory:
    """
    Validate that the AI output is a valid content category.
    Throws ValueError if the output is not a valid category.
    """
    cleaned_output = output.strip().lower()
    if cleaned_output not in content_categories:
        raise ValueError(f"Invalid category '{cleaned_output}'. Must be one of: {', '.join(content_categories)}")
    return cleaned_output


async def detect_content_category(content: str) -> ContentCategory:
    """
    Detect the category of the given content using Gemini Flash.
    """
    client = get_gemini()

    model = client.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=detect_category_prompt(content),
        generation_config=client.GenerationConfig(
            temperature=0.1,
            max_output_tokens=30,
            response_mime_type="text/plain",
        ),
    )

    response = model.generate_content(["Now, please categorize the content."])
    if not response.text:
        raise Exception("Error obtaining response from Gemini Flash")

    return validate_category_output(response.text)
