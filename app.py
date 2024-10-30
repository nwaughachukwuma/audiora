import asyncio

import streamlit as st

from src.uis.audioui import audioui
from src.uis.chatui import chatui
from src.utils.session_state import init_session_state


async def main():
    init_session_state()

    # Configure page
    # st.set_page_config(page_title="AudioCastr", page_icon="🎧", layout="wide")

    # Sidebar for content type selection
    st.sidebar.title("Audiocast Info")

    if st.session_state.content_category:
        st.sidebar.subheader(
            f"Content Category: {st.session_state.content_category.capitalize()}"
        )

    # Main chat interface
    st.title("🎧 AudioCastr")

    # Declare chat interface container
    uichat = st.empty()
    if not st.session_state.user_specification:
        with uichat.container():
            await chatui(uichat)
    else:
        await audioui(uichat)


if __name__ == "__main__":
    asyncio.run(main())
