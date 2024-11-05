import os

import streamlit as st
from pydub import AudioSegment

from services.storage import BLOB_BASE_URI, StorageManager
from shared_utils_pkg.waveform_utils import WaveformUtils


def render_waveform(session_id: str, audio_path: str, autoplay=False):
    """Render waveform visualization from audio file."""
    waveform_utils = WaveformUtils(session_id, audio_path)
    tmp_vid_path = waveform_utils.get_tmp_video_path()

    video_path = None
    if os.path.exists(tmp_vid_path):
        try:
            mp4_version = AudioSegment.from_file(str(tmp_vid_path), "mp4")
            if mp4_version.duration_seconds > 0:
                video_path = tmp_vid_path
        except Exception:
            os.remove(tmp_vid_path)
    else:
        blobname = f"{session_id}.mp4"
        exists = StorageManager().check_blob_exists(BLOB_BASE_URI, blobname)
        if exists:
            video_path = StorageManager().download_from_gcs(blobname)

    try:
        if not video_path:
            with st.spinner("Generating waveform visualization..."):
                video_path = waveform_utils.generate_waveform_video(tmp_vid_path)
                waveform_utils.save_waveform_video_to_gcs(str(video_path))

        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()
            st.video(video_bytes, autoplay=autoplay)

        download_waveform_video(str(video_path))
    except Exception as e:
        st.error(f"Error generating visualization: {str(e)}")


def download_waveform_video(video_path: str):
    """Download video with waveform"""
    gen_video, _ = st.columns(2)
    with gen_video:
        with open(video_path, "rb") as f:
            st.download_button(
                label="Download Video with waveform",
                data=f,
                file_name="audio_visualization.mp4",
                mime="video/mp4",
                use_container_width=True,
            )
