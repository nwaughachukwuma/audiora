import asyncio
import uuid
from typing import List, Literal, TypedDict, cast

import streamlit as st

from src.utils.audiocast_request import evaluate_final_response
from src.utils.chat_thread import handle_example_prompt, handle_user_prompt
from src.utils.chat_utils import AudiocastCategory, display_example_cards
from src.utils.render_audiocast import render_audiocast
from src.utils.render_chat import render_chat_history

MessageRole = Literal["user", "assistant", "ai", "human"]


class ChatMessage(TypedDict):
    role: MessageRole
    content: str


async def main():
    # Initialize session state
    if "chat_session_id" not in st.session_state:
        st.session_state.chat_session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = cast(List[ChatMessage], [])
    if "current_audiocast" not in st.session_state:
        st.session_state.current_audiocast = None
    if "example_prompt" not in st.session_state:
        st.session_state.example_prompt = None
    if "prompt" not in st.session_state:
        st.session_state.prompt = None
    if "content_type" not in st.session_state:
        st.session_state.content_type = cast(AudiocastCategory | None, None)

    # Configure page
    st.set_page_config(page_title="AudioCaster", page_icon="🎧", layout="wide")

    # Sidebar for content type selection
    st.sidebar.title("Audiocast Info")
    if st.session_state.content_type:
        st.sidebar.subheader(
            f"Content Category: {st.session_state.content_type.capitalize()}"
        )

    # Main chat interface
    st.title("🎧 AudioCaster")
    st.write(
        "Tell me what you'd like to listen to, and I'll create an audiocast for you!"
    )

    if st.session_state.messages:
        render_chat_history()
    else:
        # Display example prompt cards
        if not st.session_state.example_prompt and not st.session_state.prompt:
            display_example_cards()

    # Chat input for custom prompts
    if prompt := st.chat_input("What would you like to listen to?"):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.prompt = prompt
        st.rerun()

    if st.session_state.content_type:
        content_type = st.session_state.content_type

        with st.container():
            if st.session_state.example_prompt:
                handle_example_prompt(content_type)

        with st.container():
            if st.session_state.prompt:
                prompt = st.session_state.prompt
                st.session_state.prompt = None

                ai_message = handle_user_prompt(prompt, content_type)

                if isinstance(ai_message, str):
                    evaluate_final_response(ai_message, content_type)

        # Display current audiocast if available
        if st.session_state.current_audiocast:
            await render_audiocast()


if __name__ == "__main__":
    asyncio.run(main())
