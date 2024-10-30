import asyncio

import streamlit as st

from src.uis.audioui import audioui
from src.uis.chatui import chatui
from src.utils.session_state import init_session_state


async def main():
    st.set_page_config(page_title="Audiora", page_icon="🎧", layout="wide")

    st.title("🎧 Audiora")
    st.subheader("Listen to anything, anytime, leveraging AI")
    st.sidebar.info("A VeedoAI project. (c) 2024")

    # Sidebar for content type selection
    st.sidebar.title("Audiocast Info")

    init_session_state()

    if st.session_state.content_category:
        st.sidebar.subheader(
            f"Content Category: {st.session_state.content_category.capitalize()}"
        )
    else:
        st.sidebar.markdown(
            "> Your preferences and audiocast metadata will appear here"
        )

    # Declare chat interface container
    uichat = st.empty()
    if not st.session_state.user_specification:
        with uichat.container():
            await chatui(uichat)
    else:
        await audioui(uichat)


if __name__ == "__main__":
    asyncio.run(main())
