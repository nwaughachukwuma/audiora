import streamlit as st

from src.env_var import APP_URL


async def create_audiocast():
    pass


async def render_audiocast():
    """
    Render the audiocast based on the user's specifications
    - Display current audiocast if available
    """
    st.header("Your Audiocast")

    # Audio player
    st.audio(st.session_state.current_audiocast["audio_url"])

    # Transcript
    with st.expander("Show Transcript"):
        st.write(st.session_state.current_audiocast["transcript"])

    # Metadata
    st.sidebar.subheader("Audiocast Info")
    st.sidebar.json(st.session_state.current_audiocast["metadata"])

    # Share button
    share_url = f"{APP_URL}/audiocast/{st.session_state.current_audiocast['uuid']}/{st.session_state.current_audiocast['slug']}"
    st.sidebar.text_input("Share this audiocast:", share_url)
