import pyperclip
import streamlit as st
from src.utils.render_audiocast_utils import (
    GenerateAudiocastDict,
    render_audiocast_handler,
)
from src.utils.session_state import reset_session


def render_audiocast(session_id: str):
    """
    Render the audiocast based on the user's preferences
    - Display current audiocast if available
    """
    st.markdown("#### Your Audiocast")
    current_audiocast: GenerateAudiocastDict = st.session_state.current_audiocast

    share_url = render_audiocast_handler(session_id, current_audiocast)

    share_col, restart_row = st.columns(2, vertical_alignment="bottom")

    with share_col:
        if st.button("Copy Share link", use_container_width=True):
            pyperclip.copy(share_url)
            st.session_state.show_copy_success = True

    with restart_row:
        # New audiocast button
        if st.button("Generate New Audiocast", use_container_width=True):
            reset_session()
            st.rerun()

    if st.session_state.get("show_copy_success", False):
        st.session_state.show_copy_succes = False
        st.success("Share link copied successfully!", icon="✅")
