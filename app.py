import asyncio

import streamlit as st

from src.utils.chat_thread import (
    evaluate_final_response,
    handle_example_prompt,
    handle_user_prompt,
    use_audiocast_request,
)
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

    # Declare chat interface container
    uichat = st.empty()

    if not st.session_state.user_specification:
        with uichat.container():
            st.write(
                "Tell me what you'd like to listen to, and I'll create an audiocast for you!"
            )

            if st.session_state.messages:
                render_chat_history()
            elif not st.session_state.example_prompt and not st.session_state.prompt:
                display_example_cards()

            if st.session_state.content_category:
                content_category = st.session_state.content_category

                if st.session_state.example_prompt:
                    handle_example_prompt(content_category)

                if st.session_state.prompt:
                    prompt = st.session_state.prompt
                    st.session_state.prompt = None
                    ai_message = handle_user_prompt(prompt, content_category)

                    if isinstance(ai_message, str):
                        await evaluate_final_response(ai_message, content_category)

            # Chat input for custom prompts
            if prompt := uichat.chat_input("What would you like to listen to?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.prompt = prompt
                st.rerun()
    else:
        uichat.empty()
        uichat = st.empty()
        if not st.session_state.current_audiocast:
            uichat.info("Using your audiocast specifications")

            summary = st.session_state.user_specification
            content_category = st.session_state.content_category
            await use_audiocast_request(summary, content_category)
        else:
            st.info("Audiocast generation completed!")
            render_audiocast()


if __name__ == "__main__":
    asyncio.run(main())
