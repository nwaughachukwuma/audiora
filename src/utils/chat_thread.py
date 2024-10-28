import streamlit as st

from src.utils.chat_utils import (
    ContentCategory,
    SessionChatMessage,
    SessionChatRequest,
)
from src.utils.main_utils import chat


def generate_stream_response(prompt: str, content_category: ContentCategory):
    with st.spinner("Generating response..."):
        response_generator = chat(
            st.session_state.chat_session_id,
            SessionChatRequest(
                message=SessionChatMessage(role="user", content=prompt),
                content_category=content_category,
            ),
        )

    return response_generator


def handle_example_prompt(content_category: ContentCategory):
    """Handle selected example prompt"""
    prompt = st.session_state.example_prompt

    with st.chat_message("assistant"):
        response_generator = generate_stream_response(prompt, content_category)
        ai_message = st.write_stream(response_generator)
        st.session_state.example_prompt = None

        if ai_message:
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_message}
            )
            st.rerun()
        else:
            st.error("Failed to generate AI response. Please try again.")


def handle_user_prompt(prompt: str, content_category: ContentCategory):
    """
    Handle user input prompt
    """
    with st.chat_message("assistant"):
        response_generator = generate_stream_response(prompt, content_category)
        ai_message = st.write_stream(response_generator)

        if ai_message:
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_message}
            )

        return ai_message
