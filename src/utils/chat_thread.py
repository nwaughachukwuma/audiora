import asyncio
import re

import streamlit as st

from src.utils.chat_utils import (
    ContentCategory,
    SessionChatMessage,
    SessionChatRequest,
)
from src.utils.main_utils import GenerateAudioCastRequest, chat, generate_audiocast
from src.utils.session_state import reset_session

termination_prefix = "Ok, thanks for clarifying!"
termination_suffix = "Please click the button below to start generating the audiocast."


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


async def evaluate_final_response(ai_message: str, content_category: ContentCategory):
    """
    Evaluate if the ai_message is the final response from the ai model
    """
    st.markdown(
        """
        <style>
            div[data-testid="stColumn"]:nth-of-type(1) .stButton button {
                background-color: #059669;
                color: #d1fae5;
            }
            div[data-testid="stColumn"]:nth-of-type(1) .stButton button:hover {
                border-color: #059669;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )
    termination = termination_suffix.lower() in ai_message.lower()
    if not termination:
        return st.rerun()

    summary = re.sub(termination_prefix, "", ai_message, flags=re.IGNORECASE)
    summary = re.sub(termination_suffix, "", summary, flags=re.IGNORECASE)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "Generate Audiocast",
            use_container_width=True,
            on_click=onclick_generate_audiocast,
            args=(summary, content_category),
        ):
            pass
    with col2:
        if st.button("Restart", use_container_width=True, on_click=reset_session):
            pass


# Use a class here
def onclick_generate_audiocast(summary: str, content_category: ContentCategory):
    st.session_state.generating_audiocast = True

    async def wrapper():
        await use_audiocast_request(summary, content_category)

    asyncio.run(wrapper())


async def use_audiocast_request(summary: str, content_category: ContentCategory):
    """
    Call audiocast creating workflow

    Args:
        summary (str): user request summary or user specification
        content_category (ContentCategory): content category
    """
    with st.spinner("Generating your audiocast..."):
        audiocast_response = await generate_audiocast(
            GenerateAudioCastRequest(
                summary=summary,
                category=content_category,
            )
        )
        print(f"Generate AudioCast Response: {audiocast_response}")
        st.session_state.current_audiocast = audiocast_response
        st.rerun()
