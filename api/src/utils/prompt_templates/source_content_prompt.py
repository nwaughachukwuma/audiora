from utils.chat_utils import ContentCategory, category_qualifiers


def get_content_source_prompt(category: ContentCategory, summary: str):
    return f"""Generate {category_qualifiers[category]} content for {summary}.

    Primary Objectives:
    1. Develop content that precisely matches the specified {category} format
    2. Maintain unwavering focus on the user's original request
    3. Ensure every element directly serves the core purpose

    Content Development Guidelines:
    1. Blend elements from these sources while maintaining relevance:
        - Historical references and classical works
        - Contemporary examples and modern context
        - Timeless principles and current applications

    Quality Control Parameters:
    1. Length: Create content that is:
        - Comprehensive enough to fulfill the request completely
        - Concise enough to maintain engagement
        - No unnecessary elaboration or tangents

    2. Engagement Criteria:
        - Maintain consistent quality throughout
        - Ensure natural flow and logical progression
        - Use clear transitions between topics

    3. Creative Elements:
        - Add creative flourishes only when they enhance understanding
        - Include humor only if it strengthens the core message
        - Keep all embellishments strictly relevant to the topic

    4. Content Augmentation Rules:
        - Only add information that directly supports the main topic
        - Verify each addition provides clear value
        - Maintain thematic consistency throughout

    Remember: Every word must serve the user's original purpose. If in doubt, prioritize relevance over creativity.
    """
