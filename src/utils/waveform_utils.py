import os
import tempfile
from pathlib import Path

import streamlit as st
from pydub import AudioSegment
from seewav import visualize


def generate_waveform_video(output_path: Path, audio_path: str) -> Path:
    """Generate waveform video from audio file using SeeWav."""
    with tempfile.TemporaryDirectory() as temp_dir:
        visualize(
            audio=Path(audio_path),
            tmp=Path(temp_dir),
            out=output_path,
            bars=60,
            speed=4,
            time=0.4,
            # rate=60,
            size=(120, 68),
            fg_color=(0.0, 1.0, 0.6),  # Bright green. Try 0.2 0.2 0.2 for dark green
            bg_color=(0.05, 0.05, 0.05),  # Near black
        )
        return output_path


def render_waveform(session_id: str, audio_path: str):
    """Render waveform visualization from audio file."""
    tmp_directory = Path("/tmp/audiora/waveforms")
    tmp_directory.mkdir(parents=True, exist_ok=True)
    tmp_vid_path = tmp_directory / f"{session_id}.mp4"

    video_path = None
    if os.path.exists(tmp_vid_path):
        try:
            mp4_version = AudioSegment.from_file(str(tmp_vid_path), "mp4")
            if mp4_version.duration_seconds > 0:
                video_path = tmp_vid_path
        except Exception:
            os.remove(tmp_vid_path)

    try:
        if not video_path:
            with st.spinner("Generating waveform visualization..."):
                video_path = generate_waveform_video(tmp_vid_path, audio_path)

        # st.video(str(video_path), autoplay=True)
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()
            st.video(video_bytes, autoplay=True)

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
