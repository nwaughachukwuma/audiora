import tempfile
from pathlib import Path

from seewav import visualize

from src.services.storage import StorageManager


class WaveformUtils:
    def __init__(self, session_id: str, audio_path: str):
        self.session_id = session_id
        self.audio_path = audio_path

    def run_all(self):
        """
        1. Generate a waveform video from the audio file
        2. Upload it to Google Cloud Storage.
        """
        tmp_path = self.get_tmp_video_path()
        self.generate_waveform_video(tmp_path)
        self.save_waveform_video_to_gcs(str(tmp_path))

    def get_tmp_video_path(self):
        """
        Get temporary video path for waveform visualization.
        """
        tmp_directory = Path("/tmp/audiora/waveforms")
        tmp_directory.mkdir(parents=True, exist_ok=True)
        tmp_vid_path = tmp_directory / f"{self.session_id}.mp4"

        return tmp_vid_path

    def save_waveform_video_to_gcs(self, video_path: str):
        """Ingest waveform visualization to GCS."""
        full_path = StorageManager().upload_video_to_gcs(video_path, f"{self.session_id}.mp4")
        return full_path

    def generate_waveform_video(self, output_path: Path) -> Path:
        """Generate waveform video from audio file using SeeWav."""
        with tempfile.TemporaryDirectory() as temp_dir:
            visualize(
                audio=Path(self.audio_path),
                tmp=Path(temp_dir),
                out=output_path,
                bars=60,
                speed=4,
                time=0.4,
                # rate=60,
                # size=(120, 68),
                fg_color=(0.0, 1.0, 0.6),  # Bright green. Try 0.2 0.2 0.2 for dark green
                bg_color=(0.05, 0.05, 0.05),  # Near black
            )
            return output_path
