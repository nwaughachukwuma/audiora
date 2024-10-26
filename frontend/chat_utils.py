from typing import Any, Callable, Dict, List, Literal, Optional

import httpx
import streamlit as st
from env_var import BACKEND_URL

ContentType = Literal["story", "podcast", "sermon", "science"]

content_types: List[ContentType] = ["story", "podcast", "sermon", "science"]

content_examples: Dict[ContentType, str] = {
    "story": "Tell me a story about a magical kingdom with dragons and wizards.",
    "podcast": "Create a podcast about the history of space exploration.",
    "sermon": "Write a sermon about finding peace in times of trouble.",
    "science": "Explain the concept of black holes in simple terms.",
}


def chat_request(
    prompt: str,
    content_type: ContentType,
    on_finish: Optional[Callable[[str], Any]] = None,
):
    """
    Send a chat request to the backend server and return the AI response.
    """
    response = httpx.post(
        f"{BACKEND_URL}/api/chat/{st.session_state.chat_session_id}",
        json={
            "message": {"role": "user", "content": prompt},
            "content_type": content_type,
        },
        timeout=None,
    )

    response.raise_for_status()
    return response.iter_lines()
