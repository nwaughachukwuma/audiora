import re
from typing import TypedDict

import pyperclip
import streamlit as st

from src.env_var import APP_URL
from src.utils.session_state import reset_session
from src.utils.waveform_utils import download_waveform_video, render_waveform


class GenerateAudiocastDict(TypedDict):
    url: str
    script: str
    source_content: str
    created_at: str | None


def parse_ai_script(ai_script: str):
    matches = re.findall(r"<(Speaker\d+)>(.*?)</Speaker\d+>", ai_script, re.DOTALL)
    return "\n\n".join([f"**{speaker}**: {content}" for speaker, content in matches])


def render_audiocast(session_id: str):
    """
    Render the audiocast based on the user's preferences
    - Display current audiocast if available
    """
    st.markdown("#### Your Audiocast")
    current_audiocast: GenerateAudiocastDict = st.session_state.current_audiocast

    # Audio player
    st.audio(current_audiocast["url"])

    # Create placeholder for visualization
    with st.expander("Show Waveform Visualization"):
        viz = st.empty()
        with viz.container():
            try:
                video_path = render_waveform(session_id, current_audiocast["url"])
                if video_path:
                    # Download video
                    download_waveform_video(str(video_path))
            except Exception as e:
                st.error(f"Error rendering waveform: {str(e)}")

    # Transcript
    with st.expander("Show Transcript"):
        st.markdown(parse_ai_script(current_audiocast["script"]))

    # Metadata
    st.sidebar.subheader("Audiocast Source")
    st.sidebar.markdown(current_audiocast["source_content"])

    share_url = f"{APP_URL}/audiocast?session_id={session_id}"
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
