import asyncio
from pathlib import Path

import pyperclip
import streamlit as st

from src.env_var import APP_URL
from src.utils.main_utils import get_audiocast
from src.utils.render_audiocast import parse_ai_script
from src.utils.waveform_utils import download_waveform_video, render_waveform


def navigate_to_home():
    main_script = str(Path(__file__).parent.parent / "app.py")
    st.switch_page(main_script)


async def render_audiocast_page():
    st.set_page_config(page_title="Audiora | Share Page", page_icon="🎧")

    session_id = st.query_params.get("session_id")

    if session_id:
        # Display audiocast content
        st.title("🎧 Audiora")
        st.subheader("Share Page ")
        st.markdown(f"#### Viewing audiocast: {session_id}")

        try:
            with st.spinner("Loading audiocast..."):
                audiocast = get_audiocast(session_id)

                # Audio player
                st.audio(audiocast["url"])

                # Create placeholder for visualization
                with st.expander("Show Waveform Visualization"):
                    viz = st.empty()
                    with viz.container():
                        try:
                            video_path = render_waveform(session_id, audiocast["url"])
                            if video_path:
                                # Download video
                                download_waveform_video(str(video_path))
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

        cola, _ = st.columns([3, 5])
        with cola:
            if st.button("← Back to Home", use_container_width=True):
                navigate_to_home()


if __name__ == "__main__":
    asyncio.run(render_audiocast_page())
