from typing import TypedDict

import streamlit as st

from src.env_var import APP_URL


class GenerateAudiocastDict(TypedDict):
    uuid: str
    slug: str
    url: str
    script: str
    source_content: str


async def create_audiocast():
    pass


async def render_audiocast():
    """
    Render the audiocast based on the user's specifications
    - Display current audiocast if available
    """
    st.header("Your Audiocast")
    current_audiocast: GenerateAudiocastDict = st.session_state.current_audiocast

    # Audio player
    # st.audio(current_audiocast["url"])

    # Transcript
    with st.expander("Show Transcript"):
        st.write(current_audiocast["script"])

    # Metadata
    st.sidebar.subheader("Audiocast Info")
    st.sidebar.markdown(f"> {current_audiocast['source_content']}")

    # Share button
    share_url = (
        f"{APP_URL}/audiocast/{current_audiocast['uuid']}/{current_audiocast['slug']}"
    )
    st.sidebar.text_input("Share this audiocast:", share_url)
