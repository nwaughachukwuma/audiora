from queue import Queue

import streamlit as st

from shared_utils_pkg.session_manager import SessionManager


async def subscribe_to_audio_generation(session_id: str):
    """Subscribe to audio generation metadata"""
    q = Queue()
    db = SessionManager(session_id)
    doc_watch = db.subscribe_to_metadata_info(
        lambda info: info and q.put(info, block=False)
    )

    with st.empty():
        while True:
            try:
                info = q.get(timeout=1)
                if not info:
                    break
                st.info(info)
            except Exception:
                break

    doc_watch.unsubscribe()
