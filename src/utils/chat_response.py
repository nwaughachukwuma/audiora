import streamlit as st

from src.utils.chat_utils import ChatMessage, ContentType, SessionChatRequest
from src.utils.main_utils import chat


def generate_stream_response(prompt: str, content_type: ContentType):
    with st.spinner("Generating response..."):
        response_generator = chat(
            st.session_state.chat_session_id,
            SessionChatRequest(
                message=ChatMessage(role="user", content=prompt),
                content_type=content_type,
            ),
        )

    return response_generator
