import asyncio

import streamlit as st

from src.utils.audiocast_request import evaluate_final_response
from src.utils.chat_thread import handle_example_prompt, handle_user_prompt
from src.utils.chat_utils import display_example_cards
from src.utils.render_audiocast import render_audiocast
from src.utils.render_chat import render_chat_history
from src.utils.session_state import init_session_state


async def main():
    init_session_state()

    # Configure page
    st.set_page_config(page_title="AudioCaster", page_icon="🎧", layout="wide")

    # Sidebar for content type selection
    st.sidebar.title("Audiocast Info")
    if st.session_state.content_category:
        st.sidebar.subheader(
            f"Content Category: {st.session_state.content_category.capitalize()}"
        )

    # Main chat interface
    st.title("🎧 AudioCaster")

    if st.session_state.generating_audiocast:
        if st.session_state.current_audiocast:
            render_audiocast()
    else:
        st.write(
            "Tell me what you'd like to listen to, and I'll create an audiocast for you!"
        )
        if st.session_state.messages:
            render_chat_history()
        else:
            if not st.session_state.example_prompt and not st.session_state.prompt:
                display_example_cards()

        # Chat input for custom prompts
        if prompt := st.chat_input("What would you like to listen to?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.prompt = prompt
            st.rerun()

    if st.session_state.content_category:
        content_category = st.session_state.content_category

        with st.container():
            if st.session_state.example_prompt:
                handle_example_prompt(content_category)

        with st.container():
            if st.session_state.prompt:
                prompt = st.session_state.prompt
                st.session_state.prompt = None

                ai_message = handle_user_prompt(prompt, content_category)

                if isinstance(ai_message, str):
                    await evaluate_final_response(ai_message, content_category)


if __name__ == "__main__":
    asyncio.run(main())
