import httpx
import streamlit as st

from src.env_var import BACKEND_URL
from src.utils.chat_utils import ContentType


def evaluate_final_response(ai_message: str, content_type: ContentType):
    condition = True
    if condition:
        generate_audiocast(ai_message, content_type)


def generate_audiocast(prompt: str, content_type: ContentType):
    if st.button("Generate Audiocast"):
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
