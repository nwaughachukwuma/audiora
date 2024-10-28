import asyncio
import re
import uuid

import streamlit as st

from src.utils.chat_utils import ContentCategory
from src.utils.main_utils import GenerateAudioCastRequest, generate_audiocast


def reset_session():
    """Reset all session state"""
    st.session_state.messages = []
    st.session_state.chat_session_id = str(uuid.uuid4())
    st.session_state.current_audiocast = None

    st.session_state.example_prompt = None
    st.session_state.prompt = None
    st.session_state.generating_audiocast = False
    st.cache_data.clear()

    st.rerun()


termination_prefix = "Ok, thanks for clarifying!"
termination_suffix = "Please click the button below to start generating the audiocast."


async def evaluate_final_response(ai_message: str, content_category: ContentCategory):
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

    def onclick_generate_audiocast():
        st.session_state.generating_audiocast = True

        async def wrapper():
            await use_audiocast_request(prompt, content_category)

        asyncio.run(wrapper())

    termination = termination_suffix.lower() in ai_message.lower()
    if not termination:
        return st.rerun()

    prompt = re.sub(termination_prefix, "", ai_message, flags=re.IGNORECASE)
    prompt = re.sub(termination_suffix, "", prompt, flags=re.IGNORECASE)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "Generate Audiocast",
            use_container_width=True,
            on_click=onclick_generate_audiocast,
        ):
            pass
    with col2:
        if st.button("Restart", use_container_width=True, on_click=reset_session):
            pass


async def use_audiocast_request(prompt: str, content_category: ContentCategory):
    """
    Call audiocast creating workflow
    """
    with st.container():
        with st.spinner("Generating your audiocast..."):
            # Generate audiocast
            audiocast_response = await generate_audiocast(
                GenerateAudioCastRequest(
                    summary=prompt,
                    category=content_category,
                )
            )
            print(f"Generate AudioCast Response: {audiocast_response}")
            st.session_state.current_audiocast = audiocast_response
            st.rerun()
