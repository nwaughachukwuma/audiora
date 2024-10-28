import re
import uuid

import streamlit as st

from src.utils.chat_utils import ContentCategory
from src.utils.main_utils import GenerateAudioCastRequest
from src.utils.main_utils import generate_audiocast as _generate_audiocast

termination_prefix = "Ok, thanks for clarifying!"
termination_suffix = "Please click the button below to start generating the audiocast."


def reset_session():
    # Reset all session state
    st.session_state.messages = []
    st.session_state.chat_session_id = str(uuid.uuid4())
    st.session_state.current_audiocast = None

    st.session_state.example_prompt = None
    st.session_state.prompt = None
    st.cache_data.clear()


async def evaluate_final_response(ai_message: str, content_category: ContentCategory):
    termination = termination_suffix.lower() in ai_message.lower()
    if not termination:
        return st.rerun()

    prompt = re.sub(termination_prefix, "", ai_message, flags=re.IGNORECASE)
    prompt = re.sub(termination_suffix, "", prompt, flags=re.IGNORECASE)

    # Add CSS for colored buttons
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

    col1, col2 = st.columns(2)

    with col1:
        await generate_audiocast(prompt, content_category)

    with col2:
        if st.button("Restart", use_container_width=True, on_click=reset_session):
            st.rerun()


async def generate_audiocast(prompt: str, content_category: ContentCategory):
    if st.button("Generate Audiocast", use_container_width=True):
        with st.spinner("Generating your audiocast..."):
            # Generate audiocast
            audiocast_response = await _generate_audiocast(
                GenerateAudioCastRequest(
                    summary=prompt,
                    category=content_category,
                )
            )

            print(f"Generate AudioCast Responnse: {audiocast_response}")

            st.session_state.current_audiocast = audiocast_response
            st.rerun()
