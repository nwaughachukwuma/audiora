import asyncio

import streamlit as st
from _init_project import print_project_meta

from src.utils.custom_components import copy_button
from src.utils.render_audiocast_utils import (
    get_audiocast,
    navigate_to_home,
    render_audiocast_handler,
)

print_project_meta()


async def render_audiocast_page():
    st.set_page_config(page_title="Audiora | Share Page", page_icon="🎧", layout="wide")
    st.sidebar.info("A VeedoAI project. (c) 2024")

    session_id = st.query_params.get("session_id")

    if session_id:
        # Display audiocast content
        st.title("🎧 Audiora")
        st.subheader("Share Page ")
        st.markdown(f"##### Viewing audiocast: _{session_id}_")

        st.sidebar.info("A VeedoAI project. (c) 2024")

        try:
            with st.spinner("Loading audiocast..."):
                audiocast = get_audiocast(session_id)

            if audiocast["created_at"]:
                st.markdown(f"> Created: {audiocast["created_at"]}")

            share_url = render_audiocast_handler(session_id, audiocast)

            share_col, restart_row = st.columns(2, vertical_alignment="center")
            with share_col:
                copy_button(share_url, "Copy Share Link")

            with restart_row:
                if st.button("Create your Audiocast", use_container_width=True):
                    navigate_to_home()

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
