import re
from pathlib import Path
from typing import TypedDict

import streamlit as st

from src.env_var import APP_URL
from src.utils.waveform_utils import render_waveform


def navigate_to_home():
    main_script = str(Path(__file__).parent.parent / "app.py")
    st.switch_page(main_script)


def parse_ai_script(ai_script: str):
    matches = re.findall(r"<(Speaker\d+)>(.*?)</Speaker\d+>", ai_script, re.DOTALL)
    return "\n\n".join([f"**{speaker}**: {content}" for speaker, content in matches])


class GenerateAudiocastDict(TypedDict):
    url: str
    script: str
    source_content: str
    created_at: str | None


def render_audiocast_handler(session_id: str, audiocast: GenerateAudiocastDict):
    # Audio player
    st.audio(audiocast["url"])

    # Create placeholder for visualization
    with st.expander("Show Waveform Visualization"):
        # with st.container():
        try:
            render_waveform(session_id, audiocast["url"])
        except Exception as e:
            st.error(f"Error rendering waveform: {str(e)}")

    # Transcript
    with st.expander("Show Transcript"):
        st.markdown(parse_ai_script(audiocast["script"]))

    # Metadata
    st.sidebar.subheader("Audiocast Source")
    st.sidebar.markdown(audiocast["source_content"])

    share_url = f"{APP_URL}/audiocast?session_id={session_id}"
    st.text_input("Share this audiocast:", share_url)

    return share_url
