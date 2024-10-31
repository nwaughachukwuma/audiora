import asyncio
from pathlib import Path

import streamlit as st

from src.utils.main_utils import get_audiocast_uri


def navigate_to_home():
    main_script = str(Path(__file__).parent.parent / "app.py")
    st.switch_page(main_script)


async def render_audiocast_page():
    st.set_page_config(page_title="Audiora | Share Page", page_icon="🎧")

    audiocast_id = st.query_params.get("session_id")

    if audiocast_id:
        # Display audiocast content
        st.title("🎧 Audiocast Player")
        st.write(f"Playing audiocast: {audiocast_id}")

        try:
            with st.spinner("Loading audiocast..."):
                audio_path = get_audiocast_uri(audiocast_id)
                st.audio(audio_path)

                # TODO: Fetch audiocast metadata from the database
                st.subheader("Audiocast Details")
                st.write("Created: 2024-03-20")

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
