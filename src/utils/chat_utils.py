from typing import Dict, List, Literal

import streamlit as st
from pydantic import BaseModel

ContentCategory = Literal[
    "podcast",
    "soundbite",
    "sermon",
    "audiodrama",
    "commentary",
    "lecture",
    "voicenote",
    "interview",
]

audiocast_categories: List[ContentCategory] = [
    "podcast",
    "soundbite",
    "sermon",
    "audiodrama",
    "commentary",
    "lecture",
    "voicenote",
    "interview",
]

content_examples: Dict[ContentCategory, str] = {
    "podcast": "Create a podcast exploring the intersection of ancient philosophy and artificial intelligence.",
    "sermon": "Write a sermon connecting the teachings of Augustine with modern digital ethics.",
    "audiodrama": "A reimagining of Homer's Odyssey set in a cyberpunk future.",
    "lecture": "A lecture comparing Shakespeare's influence on modern social media communication.",
    "commentary": "A commentary on how Classical music influences contemporary electronic genres.",
    "voicenote": "A personal reflection on reading Plato's Republic in today's political climate.",
    "interview": "An interview with an archaeologist using AI to uncover ancient Roman artifacts.",
    "soundbite": "A quick take on how ancient Greek democracy shapes modern blockchain governance.",
}


class SessionChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class SessionChatRequest(BaseModel):
    content_category: ContentCategory
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
    for content_category, example in content_examples.items():
        with col1 if content_category in [
            "podcast",
            "soundbite",
            "sermon",
            "audiodrama",
        ] else col2:
            if st.button(example, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": example})
                st.session_state.example_prompt = example
                st.session_state.content_category = content_category

                st.rerun()
