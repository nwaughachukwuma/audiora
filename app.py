import asyncio
import uuid
from typing import List, Literal, TypedDict, cast

import streamlit as st

from src.env_var import APP_URL
from src.utils.audiocast_request import evaluate_final_response
from src.utils.chat_thread import handle_example_prompt, handle_user_prompt
from src.utils.chat_utils import content_types, display_example_cards

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

    # Configure page
    st.set_page_config(page_title="AudioCaster", page_icon="🎧", layout="wide")

    # Sidebar for content type selection
    st.sidebar.title("AudioCaster")
    content_type = st.sidebar.selectbox(
        "Select Content Type",
        content_types,
        format_func=lambda x: x.title(),
    )

    # Main chat interface
    st.title("🎧 AudioCaster")
    st.write(
        "Tell me what you'd like to listen to, and I'll create an audiocast for you!"
    )

    if st.session_state.messages:
        st.info("Chat Session")
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
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
        st.header("Your Audiocast")

        # Audio player
        st.audio(st.session_state.current_audiocast["audio_url"])

        # Transcript
        with st.expander("Show Transcript"):
            st.write(st.session_state.current_audiocast["transcript"])

        # Metadata
        st.sidebar.subheader("Audiocast Info")
        st.sidebar.json(st.session_state.current_audiocast["metadata"])

        # Share button
        share_url = f"{APP_URL}/audiocast/{st.session_state.current_audiocast['uuid']}/{st.session_state.current_audiocast['slug']}"
        st.sidebar.text_input("Share this audiocast:", share_url)


if __name__ == "__main__":
    asyncio.run(main())
