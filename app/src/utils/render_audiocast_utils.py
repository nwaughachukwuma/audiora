import re
from pathlib import Path
from typing import cast

import httpx
import streamlit as st

from env_var import APP_URL, API_URL
from src.utils.render_waveform import render_waveform
from utils_pkg.audiocast_utils import GenerateAudioCastRequest, GenerateAudiocastDict
from utils_pkg.chat_utils import ContentCategory


def navigate_to_home():
    main_script = str(Path(__file__).parent.parent.parent / "index.py")
    st.switch_page(main_script)


def parse_ai_script(ai_script: str):
    matches = re.findall(r"<(Speaker\d+)>(.*?)</Speaker\d+>", ai_script, re.DOTALL)
    return "\n\n".join([f"**{speaker}**: {content}" for speaker, content in matches])


def get_audiocast(session_id: str):
    response = httpx.get(f"{API_URL}/audiocast/{session_id}", timeout=None)
    response.raise_for_status()
    return cast(GenerateAudiocastDict, response.json())


async def generate_audiocast(
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
        f"{API_URL}/audiocast/generate",
        json=audiocast_req.model_dump(),
        timeout=None,
    )
    response.raise_for_status()

    return cast(GenerateAudiocastDict, response.json())


def render_audiocast_handler(session_id: str, audiocast: GenerateAudiocastDict):
    # Audio player
    st.audio(audiocast["url"])

    # Voice waveform
    with st.expander("Show Audio Waveform"):
        try:
            render_waveform(session_id, audiocast["url"], False)
        except Exception as e:
            st.error(f"Error rendering waveform: {str(e)}")

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
