import tempfile
from pathlib import Path
from typing import Literal

from seewav import visualize

from src.services.storage import StorageManager

WaveformQuality = Literal["low", "medium", "high", "ultra"]
WaveFormSettings = {
    "low": {"bars": 40, "speed": 3, "time": 0.5, "rate": 24, "oversample": 1},
    "medium": {"bars": 60, "speed": 2, "time": 0.8, "rate": 30, "oversample": 2},
    "high": {"bars": 80, "speed": 1.5, "time": 1.0, "rate": 30, "oversample": 4},
    "ultra": {"bars": 120, "speed": 1, "time": 1.2, "rate": 60, "oversample": 8},
}


class WaveformUtils:
    def __init__(self, session_id: str, audio_path: str):
        self.session_id = session_id
        self.audio_path = audio_path

    def _get_quality_settings(self, quality: WaveformQuality = "high"):
        return WaveFormSettings.get(quality, WaveFormSettings["high"])

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

    def generate_waveform_video(self, output_path: Path, quality: WaveformQuality = "high") -> Path:
        """Generate waveform video from audio file using SeeWav with quality settings."""
        settings = self._get_quality_settings(quality)

        with tempfile.TemporaryDirectory() as temp_dir:
            visualize(
                audio=Path(self.audio_path),
                tmp=Path(temp_dir),
                out=output_path,
                bars=settings["bars"],
                speed=settings["speed"],
                time=settings["time"],
                rate=settings["rate"],
                oversample=settings["oversample"],
                # size=(120, 68),
                fg_color=(0.0, 1.0, 0.6),  # Bright green
                bg_color=(0.05, 0.05, 0.05),  # Near black
            )
            return output_path
