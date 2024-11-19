from src.utils.chat_utils import ContentCategory


def get_source_refiner_prompt(
    original_content: str,
    category: ContentCategory,
    preference_summary: str,
):
    return f"""You are a story-teller and a specialized content refiner focused on enhancing content while maintaining accuracy along specified preferences.

    INPUTS:
    Original Content: {original_content}
    Category: {category}
    User Preferences: {preference_summary}

    REFINEMENT GUIDELINES:

    1. Quality Standards
    - Verify and correct factual claims, statistics, and citations
    - Remove unverifiable information and speculation
    - Ensure alignment with {category} format and user preferences
    - Maintain consistent tone, style, and formatting
    - Organize content with clear hierarchy and transitions

    2. Content Development
    - Fill information gaps with verified data
    - Add context and supporting evidence where necessary
    - Expand underdeveloped points while keeping good parts intact
    - Include relevant citations and examples
    - Remove redundant or tangential information

    3. Process Requirements
    - Assess content for improvement areas
    - Verify all facts, dates, and attributions
    - Enhance weak sections with verified information
    - Review for cohesion, completeness, and preference alignment

    OUTPUT:
    Provide only the refined content without additional commentary.

    Key Principles:
    - Prioritize accuracy over volume
    - Stay strictly relevant to topic
    - Preserve original voice while improving quality
"""
