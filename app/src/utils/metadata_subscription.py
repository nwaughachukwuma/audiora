import asyncio

import streamlit as st

from shared_utils_pkg.session_manager import SessionManager


class SubscribeToAudioGeneration:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.info: str | None = None

    def create(self):
        """Subscribe to audio generation metadata"""

        def __handler(info: str):
            self.info = info

        db = SessionManager(self.session_id)
        return db.subscribe_to_metadata_info(__handler)

    async def _update_ui(self, read_timeout=10):
        """Update the UI with the current info attribute value."""
        timeout = 0
        container = st.empty()

        with container:
            while read_timeout > timeout:
                if self.info:
                    container.info(self.info)
                await asyncio.sleep(1)
                timeout += 1

        container.empty()
