from typing import Dict, List, Literal

import streamlit as st
from pydantic import BaseModel

ContentType = Literal["podcast", "story", "sermon", "science"]

content_types: List[ContentType] = ["podcast", "story", "sermon", "science"]

content_examples: Dict[ContentType, str] = {
    "story": "Tell me a story about a magical kingdom with dragons and wizards.",
    "podcast": "Create a podcast about the history of space exploration.",
    "sermon": "Write a sermon about finding peace in times of trouble.",
    "science": "A commentary on the concept of black holes.",
}


class SessionChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class SessionChatRequest(BaseModel):
    content_type: ContentType
    message: SessionChatMessage


def display_example_cards():
    """Display example content cards if there are no messages"""
    st.markdown("#### You can start with one of the following")

    # CSS for fixed-height buttons and responsive columns
    st.markdown(
        """
        <style>
            .stButton button {
                height: 125px;
                white-space: normal;
                word-wrap: break-word;
                color: #030712
            }
            @media (max-width: 960px) {
                div[data-testid="stColumn"] {
                    width: 100% !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display example content cards
    col1, col2 = st.columns(2)
    for content_type, example in content_examples.items():
        with col1 if content_type in ["story", "podcast"] else col2:
            if st.button(example, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": example})
                st.session_state.example_prompt = example

                st.rerun()
