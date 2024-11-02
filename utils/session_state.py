import uuid
from typing import List, Literal, TypedDict, cast

import streamlit as st

from utils.chat_utils import ContentCategory

MessageRole = Literal["user", "assistant", "ai", "human"]


class ChatMessage(TypedDict):
    role: MessageRole
    content: str


def init_session_state():
    """Initialize session state"""
    if "chat_session_id" not in st.session_state:
        st.session_state.chat_session_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = cast(List[ChatMessage], [])
    if "example_prompt" not in st.session_state:
        st.session_state.example_prompt = None
    if "prompt" not in st.session_state:
        st.session_state.prompt = None

    if "content_category" not in st.session_state:
        st.session_state.content_category = cast(ContentCategory | None, None)

    if "user_specification" not in st.session_state:
        st.session_state.user_specification = None
    if "current_audiocast" not in st.session_state:
        st.session_state.current_audiocast = None

    return cast(str, st.session_state.chat_session_id)


def reset_session():
    """
    Reset all session state.

    #### Client must call st.rerun()
    """
    st.session_state.chat_session_id = str(uuid.uuid4())

    st.session_state.messages = []
    st.session_state.example_prompt = None
    st.session_state.prompt = None

    st.session_state.content_category = None

    st.session_state.user_specification = None
    st.session_state.current_audiocast = None

    st.cache_data.clear()
