import asyncio
import re

import streamlit as st

from src.utils.chat_utils import ContentCategory
from src.utils.main_utils import GenerateAudioCastRequest, generate_audiocast
from src.utils.session_state import reset_session

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

    def onclick_generate_audiocast(summary: str):
        st.session_state.generating_audiocast = True

        async def wrapper():
            await use_audiocast_request(summary, content_category)

        asyncio.run(wrapper())

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
            args=(summary,),
        ):
            pass
    with col2:
        if st.button("Restart", use_container_width=True, on_click=reset_session):
            pass


async def use_audiocast_request(summary: str, content_category: ContentCategory):
    """
    Call audiocast creating workflow
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
