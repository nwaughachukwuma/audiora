import asyncio
from typing import cast

import streamlit as st

from src.utils.copy_to_clipboard import audiocast_actions
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

        st.sidebar.info("A VeedoAI project. (c) 2024")

        try:
            with st.spinner("Loading audiocast..."):
                audiocast = cast(GenerateAudiocastDict, get_audiocast(session_id))

            if audiocast["created_at"]:
                st.markdown(f"> Created: {audiocast["created_at"]}")

            share_url = render_audiocast_handler(session_id, audiocast)

            # share_col, restart_row = st.columns(2, vertical_alignment="bottom")

            # with share_col:
            #     copy_button(share_url, "Copy Share Link")
            #     # if st.button("Copy Share link", use_container_width=True):
            #     #     copy_button(share_url)
            #     # st.session_state.show_copy_success = True

            # with restart_row:
            #     if st.button("Create your Audiocast", use_container_width=True):
            #         navigate_to_home()

            audiocast_actions(share_url, "Copy Share Link")

        except Exception as e:
            st.error(f"Error loading audiocast: {str(e)}")
    else:
        st.warning("Audiocast ID is missing in the URL. Expected URL format: ?session_id=your-audiocast-id")

        st.markdown("---")

        col1, _ = st.columns([3, 5])
        with col1:
            if st.button("← Back to Home", use_container_width=True):
                navigate_to_home()


if __name__ == "__main__":
    asyncio.run(render_audiocast_page())
