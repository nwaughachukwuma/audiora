from src.utils.chat_utils import ContentCategory, category_qualifiers


def generate_source_content_prompt(category: ContentCategory, summary: str, additional_context: str):
    return f"""Generate {category_qualifiers[category]} content for {summary}.

    ADDITIONAL CONTEXT:
    {additional_context}

    Primary Objectives:
    1. Develop content that precisely matches the specified {category} format
    2. Maintain unwavering focus on the user preferences
    3. Ensure every element of the content serves the core purpose
    4. Leverage the additional context to enhance the content quality, authenticity and depth

    Content Development Guidelines:
    1. Blend elements from these sources while maintaining veracity and relevance:
        - Historical references and classical works
        - Contemporary examples and modern context
        - Timeless principles and current applications

    Quality Control Parameters:
    1. Length: Create content that is:
        - Comprehensive enough to fulfill the user preferences exhaustively
        - Long enough to maintain engagement
        - Without unnecessary elaboration or tangents

    2. Engagement Criteria:
        - Maintain consistent quality throughout
        - Ensure natural flow and logical progression
        - Use clear transitions between topics

    3. Creative Elements:
        - Add creative flourishes only when they enhance understanding
        - Include humor only if it strengthens the core message
        - Keep all embellishments strictly relevant to the topic
        - Keep the overall content authentic and factual

    4. Content Augmentation Rules:
        - Only add information that directly supports the main topic
        - Verify each addition provides clear value, without any false or misleading information
        - Maintain thematic consistency throughout
        - explicitly reference the user's preferences in the content
        - leverage the additional context to enhance for improved depth

    Remember:
    - Ignore the additional context if it does not align with or add value to the user preferences.
    - If in doubt, prioritize relevance over creativity.
    """
