from typing import TypedDict

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
    Render the audiocast based on the user's specifications
    - Display current audiocast if available
    """
    st.header("Your Audiocast")
    current_audiocast: GenerateAudiocastDict = st.session_state.current_audiocast

    # Audio player
    st.audio(current_audiocast["url"])

    # Transcript
    with st.expander("Show Transcript"):
        st.write(current_audiocast["script"])

    # Metadata
    st.sidebar.subheader("Audiocast Source")
    st.sidebar.markdown(current_audiocast["source_content"])

    share_row, _ = st.columns(2)

    with share_row:
        # Share button
        share_url = f"{APP_URL}/audiocast/{current_audiocast['uuid']}/{current_audiocast['slug']}"
        st.text_input("Share this audiocast:", share_url)

    restart_row, _ = st.columns(2)

    with restart_row:
        # New audiocast button
        if st.button("Generate New Audiocast", use_container_width=True):
            reset_session()
            st.rerun()
