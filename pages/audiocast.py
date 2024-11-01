import asyncio
from typing import cast

import pyperclip
import streamlit as st

from src.utils.main_utils import get_audiocast
from src.utils.render_audiocast_utils import (
    GenerateAudiocastDict,
    navigate_to_home,
    render_audiocast_handler,
)


async def render_audiocast_page():
    st.set_page_config(page_title="Audiora | Share Page", page_icon="🎧")

    session_id = st.query_params.get("session_id")

    if session_id:
        # Display audiocast content
        st.title("🎧 Audiora")
        st.subheader("Share Page ")
        st.markdown(f"##### Viewing audiocast: _{session_id}_")

        try:
            with st.spinner("Loading audiocast..."):
                audiocast = cast(GenerateAudiocastDict, get_audiocast(session_id))

            share_url = render_audiocast_handler(session_id, audiocast)

            share_col, restart_row = st.columns(2, vertical_alignment="bottom")

            with share_col:
                if st.button("Copy Share link", use_container_width=True):
                    pyperclip.copy(share_url)
                    st.session_state.show_copy_success = True

            with restart_row:
                if st.button("Create your Audiocast", use_container_width=True):
                    navigate_to_home()

            if st.session_state.get("show_copy_success", False):
                st.session_state.show_copy_succes = False
                st.success("Share link copied successfully!", icon="✅")

            if audiocast["created_at"]:
                st.markdown(f"> Created: {audiocast["created_at"]}")

        except Exception as e:
            st.error(f"Error loading audiocast: {str(e)}")
    else:
        st.warning(
            "Audiocast ID is missing in the URL. Expected URL format: ?session_id=your-audiocast-id"
        )

        st.markdown("---")

        col1, _ = st.columns([3, 5])
        with col1:
            if st.button("← Back to Home", use_container_width=True):
                navigate_to_home()


if __name__ == "__main__":
    asyncio.run(render_audiocast_page())
