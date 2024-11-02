import streamlit as st
from src.utils.chat_thread import (
    evaluate_final_response,
    handle_example_prompt,
    handle_user_prompt,
)
from src.utils.display_example_cards import display_example_cards
from src.utils.render_chat import render_chat_history
from streamlit.delta_generator import DeltaGenerator


async def chatui(session_id: str, uichat: DeltaGenerator):
    """
    Chat interface
    """
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
            prompt = st.session_state.example_prompt
            handle_example_prompt(session_id, prompt, content_category)

        if st.session_state.prompt:
            prompt = st.session_state.prompt
            st.session_state.prompt = None
            ai_message = handle_user_prompt(session_id, prompt, content_category)

            if isinstance(ai_message, str):
                await evaluate_final_response(ai_message, content_category)

    # Chat input for custom prompts
    if prompt := uichat.chat_input("What would you like to listen to?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.prompt = prompt
        st.rerun()
