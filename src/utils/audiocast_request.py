import re
import uuid

import httpx
import streamlit as st

from src.env_var import BACKEND_URL
from src.utils.chat_utils import ContentType

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


def evaluate_final_response(ai_message: str, content_type: ContentType):
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
        generate_audiocast(prompt, content_type)

    with col2:
        if st.button("Restart", use_container_width=True, on_click=reset_session):
            st.rerun()


def generate_audiocast(prompt: str, content_type: ContentType):
    if st.button("Generate Audiocast", use_container_width=True):
        with st.spinner("Generating your audiocast..."):
            # Generate audiocast
            audiocast_response = httpx.post(
                f"{BACKEND_URL}/api/generate-audiocast",
                json={
                    "query": prompt,
                    "type": content_type,
                    "chat_history": st.session_state.messages,
                },
            )

            if audiocast_response.status_code == 200:
                st.session_state.current_audiocast = audiocast_response.json()
                st.rerun()
