import streamlit as st

from src.utils.chat_response import generate_stream_response
from src.utils.chat_utils import (
    ContentType,
)


def handle_selected_example(content_type: ContentType):
    """Handle selected example prompt"""
    prompt = st.session_state.seleted_example

    with st.chat_message("assistant"):
        response_generator = generate_stream_response(prompt, content_type)
        ai_message = st.write_stream(response_generator)
        st.session_state.seleted_example = None

        if ai_message:
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_message}
            )
            st.rerun()
        else:
            st.error("Failed to generate AI response. Please try again.")
