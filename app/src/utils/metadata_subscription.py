from queue import Queue

import streamlit as st

from shared_utils_pkg.session_manager import SessionManager


def subscribe_to_audio_generation(session_id: str):
    """Subscribe to audio generation metadata"""
    q = Queue()

    def handler(info: str | None):
        if info:
            q.put(info, block=False)

    db = SessionManager(session_id)
    doc_watch = db.subscribe_to_metadata_info(handler)

    with st.empty():
        while True:
            try:
                info = q.get(timeout=2)
                if not info:
                    break
                st.info(info)
            except Exception:
                break

    return doc_watch
