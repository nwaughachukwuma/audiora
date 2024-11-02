import asyncio

import streamlit as st
from _init_project import print_project_meta
from uis.audioui import audioui
from uis.chatui import chatui

from utils.session_state import init_session_state

print_project_meta()


async def main():
    st.set_page_config(page_title="Audiora", page_icon="🎧", layout="wide")

    st.title("🎧 Audiora")
    st.subheader("Listen to anything, anytime, leveraging AI")
    st.sidebar.info("A VeedoAI project. (c) 2024")

    # Sidebar for content type selection
    st.sidebar.title("Audiocast Info")

    session_id = init_session_state()

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
            await chatui(session_id, uichat)
    else:
        await audioui(session_id, uichat)


if __name__ == "__main__":
    asyncio.run(main())
