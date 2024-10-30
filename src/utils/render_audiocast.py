from typing import TypedDict

import pyperclip
import streamlit as st

from src.env_var import APP_URL
from src.utils.session_state import reset_session


class GenerateAudiocastDict(TypedDict):
    uuid: str
    slug: str
    url: str
    script: str
    source_content: str


def render_audiocast():
    """
    Render the audiocast based on the user's preferences
    - Display current audiocast if available
    """
    st.markdown("#### Your Audiocast")
    current_audiocast: GenerateAudiocastDict = st.session_state.current_audiocast

    # Audio player
    st.audio(current_audiocast["url"])

    # Transcript
    with st.expander("Show Transcript"):
        st.write(current_audiocast["script"])

    # Metadata
    st.sidebar.subheader("Audiocast Source")
    st.sidebar.markdown(current_audiocast["source_content"])

    share_url = (
        f"{APP_URL}/audiocast/{current_audiocast['uuid']}/{current_audiocast['slug']}"
    )
    st.text_input("Share this audiocast:", share_url)

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
