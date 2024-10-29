import streamlit as st

from src.utils.chat_thread import (
    use_audiocast_request,
)
from src.utils.render_audiocast import render_audiocast


async def audioui(uichat=st.empty()):
    """
    Audiocast interface
    """
    uichat.chat_input("What would you like to listen to?", disabled=True)
    uichat.empty()

    if not st.session_state.current_audiocast:
        st.info("Using your audiocast specifications")
        summary = st.session_state.user_specification
        content_category = st.session_state.content_category
        await use_audiocast_request(summary, content_category)
    else:
        st.info("Audiocast generation completed!")
        render_audiocast()
