import re
from pathlib import Path
from typing import TypedDict, cast

import httpx
import streamlit as st
from pydantic import BaseModel
from src.utils.render_waveform import render_waveform

from env_var import APP_URL, SERVER_URL
from utils_pkg.chat_utils import ContentCategory


class GenerateAudioCastRequest(BaseModel):
    sessionId: str
    summary: str
    category: str


class GenerateAudioCastResponse(BaseModel):
    url: str
    script: str
    source_content: str
    created_at: str | None


class GenerateAudiocastDict(TypedDict):
    url: str
    script: str
    source_content: str
    created_at: str | None


def navigate_to_home():
    main_script = str(Path(__file__).parent.parent / "app.py")
    st.switch_page(main_script)


def parse_ai_script(ai_script: str):
    matches = re.findall(r"<(Speaker\d+)>(.*?)</Speaker\d+>", ai_script, re.DOTALL)
    return "\n\n".join([f"**{speaker}**: {content}" for speaker, content in matches])


def get_audiocast(session_id: str):
    response = httpx.post(f"{SERVER_URL}/audiocast/{session_id}", timeout=None)
    response.raise_for_status()
    return cast(GenerateAudiocastDict, response.json())


def generate_audiocast(
    session_id: str,
    summary: str,
    content_category: ContentCategory,
):
    audiocast_req = GenerateAudioCastRequest(
        sessionId=session_id,
        summary=summary,
        category=content_category,
    )
    response = httpx.post(
        f"{SERVER_URL}/audiocast/generate",
        json=audiocast_req.model_dump(),
        timeout=None,
    )
    response.raise_for_status()

    return cast(GenerateAudiocastDict, response.json())


def render_audiocast_handler(session_id: str, audiocast: GenerateAudiocastDict):
    # Audio player
    st.audio(audiocast["url"])

    st.markdown("---")

    col1, _ = st.columns([4, 1])
    with col1:

        def toggle_show_waveform():
            st.session_state.show_waveform = not st.session_state.get("show_waveform")

        button_label = (
            "Hide Waveform Visualization"
            if st.session_state.get("show_waveform")
            else "Show Waveform Visualization"
        )

        st.button(
            button_label,
            on_click=toggle_show_waveform,
            use_container_width=True,
        )

        if st.session_state.get("show_waveform"):
            try:
                render_waveform(session_id, audiocast["url"])
            except Exception as e:
                st.error(f"Error rendering waveform: {str(e)}")

    st.markdown("---")

    # Transcript
    with st.expander("Show Transcript"):
        st.markdown(parse_ai_script(audiocast["script"]))

    st.markdown("---")

    # Metadata
    st.sidebar.subheader("Audiocast Source")
    st.sidebar.markdown(audiocast["source_content"])

    share_url = f"{APP_URL}/audiocast?session_id={session_id}"
    st.text_input("Share this audiocast:", share_url)

    return share_url
