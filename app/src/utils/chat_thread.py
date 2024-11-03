import re
from typing import Any, Generator

import httpx
import streamlit as st
from src.utils.render_audiocast_utils import generate_audiocast
from src.utils.session_state import reset_session

from env_var import SERVER_URL
from utils_pkg.chat_utils import (
    ContentCategory,
    SessionChatMessage,
    SessionChatRequest,
)

termination_prefix = "Ok, thanks for clarifying!"
termination_suffix = "Please click the button below to start generating the audiocast."


def generate_stream_response(
    session_id: str,
    prompt: str,
    content_category: ContentCategory,
) -> Generator[str, Any, None]:
    with st.spinner("Generating response..."):
        session_chat = SessionChatRequest(
            message=SessionChatMessage(role="user", content=prompt),
            content_category=content_category,
        )

        response = httpx.post(
            f"{SERVER_URL}/chat/{session_id}",
            json={**session_chat.model_dump()},
            timeout=None,
        )
        response.raise_for_status()
        return response.json()


def handle_example_prompt(
    session_id: str,
    prompt: str,
    content_category: ContentCategory,
):
    """Handle selected example prompt"""

    with st.chat_message("assistant"):
        response_generator = generate_stream_response(
            session_id, prompt, content_category
        )
        ai_message = st.write_stream(response_generator)
        st.session_state.example_prompt = None

        if ai_message:
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_message}
            )
            st.rerun()
        else:
            st.error("Failed to generate AI response. Please try again.")


def handle_user_prompt(
    session_id: str,
    prompt: str,
    content_category: ContentCategory,
):
    """
    Handle user input prompt
    """
    with st.chat_message("assistant"):
        response_generator = generate_stream_response(
            session_id,
            prompt,
            content_category,
        )
        ai_message = st.write_stream(response_generator)

        if ai_message:
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_message}
            )

        return ai_message


async def evaluate_final_response(ai_message: str):
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

    # Check if the chat session should end
    end_chat_session = termination_suffix.lower() in ai_message.lower()
    if not end_chat_session:
        return st.rerun()

    summary = re.sub(termination_prefix, "", ai_message, flags=re.IGNORECASE)
    summary = re.sub(termination_suffix, "", summary, flags=re.IGNORECASE)

    col1, col2 = st.columns(2)
    with col1:

        def onclick(summary: str):
            st.session_state.user_specification = summary
            st.session_state.should_rerun = True  # Add a flag for rerun

        st.button(
            "Generate Audiocast",
            use_container_width=True,
            on_click=onclick,
            args=(summary,),
        )

        if st.session_state.get("should_rerun", False):
            st.session_state.should_rerun = False  # Reset the flag
            st.rerun()

    with col2:
        if st.button("Restart", use_container_width=True, on_click=reset_session):
            st.rerun()


async def use_audiocast_request(
    session_id: str,
    summary: str,
    content_category: ContentCategory,
):
    """
    Call audiocast creating workflow

    Args:
        summary (str): user request summary or preferences
        content_category (ContentCategory): content category
    """
    try:
        with st.spinner("Generating your audiocast..."):
            audiocast_response = await generate_audiocast(
                session_id,
                summary,
                content_category,
            )

            print(f"Generate AudioCast Response: {audiocast_response}")

            st.session_state.current_audiocast = audiocast_response
            st.session_state.messages = []  # Clear messages
            st.rerun()
    except Exception as e:
        st.warning("Error while generating your audiocast. Please start afresh!")
        st.error(f"Error generating audiocast: {str(e)}")

        st.session_state.user_specification = None
        if st.button("Restart", use_container_width=True):
            st.rerun()
