import re
from typing import List


def clean_tss_markup(input_text: str, tags: List[str] = []) -> str:
    """
    Remove unsupported TSS markup tags from the input text while preserving supported SSML tags.

    Args:
        input_text (str): The input text containing TSS markup tags.
        tags (List[str]): Optional list of additional tags to preserve.

    Returns:
        str: Cleaned text with unsupported TSS markup tags removed.
    """
    # List of SSML tags
    supported_tags = [
        "speak",
        "lang",
        "p",
        "phoneme",
        "s",
        "say-as",
        "sub",
        "prosody",
        "break",
        "emphasis",
        "mark",
    ]

    # Append additional tags to the supported tags list
    supported_tags.extend(tags)
    # Create a pattern that matches any tag not in the supported list
    pattern = r"</?(?!(?:" + "|".join(supported_tags) + r")\b)[^>]+>"
    cleaned_text = re.sub(pattern, "", input_text)

    # Remove any leftover empty lines
    cleaned_text = re.sub(r"\n\s*\n", "\n", cleaned_text)
    # Ensure closing tags for additional tags are preserved
    for tag in tags:
        cleaned_text = re.sub(
            f'<{tag}>(.*?)(?=<(?:{"|".join(tags)})>|$)',
            f"<{tag}>\\1</{tag}>",
            cleaned_text,
            flags=re.DOTALL,
        )

    return cleaned_text.strip()
