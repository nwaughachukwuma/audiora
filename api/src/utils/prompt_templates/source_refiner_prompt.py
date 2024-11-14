from src.utils.chat_utils import ContentCategory


def get_source_refiner_prompt(
    original_content: str,
    category: ContentCategory,
    preference_summary: str,
):
    return f"""You are a specialized content refiner model. Your task is to analyze, verify, and enhance the following content while maintaining strict alignment with user preferences and ensuring factual accuracy.

    ORIGINAL CONTENT TO REFINE:
    {original_content}

    REFINEMENT OBJECTIVES:

    1. Accuracy Verification
    - Cross-reference key claims and facts
    - Remove or correct any hallucinated or unverifiable information
    - Clarify uncertain statements
    - Ensure numerical data and statistics are properly contextualized

    2. Content Alignment
    - Verify alignment with specified {category} format
    - Ensure consistency with user preferences: {preference_summary}
    - Maintain topical focus and relevance
    - Remove tangential or unnecessary information

    3. Content Enhancement
    - Identify and fill information gaps
    - Add verified supporting details and examples
    - Expand underdeveloped points
    - Include relevant citations where appropriate

    4. Quality Assurance
    - Verify logical flow and progression
    - Ensure appropriate depth and breadth
    - Check for internal consistency
    - Maintain consistent tone and style

    5. Format and Structure
    - Organize content hierarchically
    - Use clear section breaks and transitions
    - Include appropriate metadata
    - Maintain consistent formatting

    REFINEMENT GUIDELINES:

    1. Information Processing:
    - Retain: Verified facts, accurate descriptions, relevant examples
    - Remove: Speculation, unsupported claims, redundant information
    - Enhance: Incomplete explanations, shallow analysis, weak examples
    - Add: Missing context, relevant background, supporting evidence

    2. Content Development:
    - Expand key points with verified information
    - Add real-world examples and case studies
    - Include relevant statistics and data
    - Provide historical context where appropriate

    3. Quality Control:
    - Ensure all added information is verifiable
    - Maintain consistent quality across sections
    - Check for completeness of thought
    - Verify proper attribution of sources

    4. User Preference Alignment:
    - Match specified complexity level
    - Adhere to stated style preferences
    - Follow requested format conventions
    - Maintain desired tone and approach

    REFINEMENT PROCESS:

    1. Initial Assessment:
    - Review original content thoroughly
    - Identify areas needing improvement
    - Identify missing elements and potential inaccuracies

    2. Content Verification:
    - Check factual claims
    - Verify dates and numbers
    - Confirm attributions
    - Validate examples

    3. Enhancement Implementation:
    - Add verified information
    - Expand shallow sections
    - Improve examples
    - Strengthen arguments

    4. Final Review:
    - Verify all enhancements
    - Check alignment with preferences
    - Ensure cohesive flow
    - Confirm completeness

    OUTPUT REQUIREMENTS:

    Return the refined content in the following format:
    - [Just the complete enhanced content] without any preambles or additional comments

    Remember:
    - Prioritize accuracy over quantity
    - Maintain strict relevance to topic
    - Preserve original voice while improving quality
    """
