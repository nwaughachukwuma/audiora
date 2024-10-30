import os
import re
from pathlib import Path
from typing import List, Union

from pydub import AudioSegment


class AudioEnhancer:
    def enhance_audio(
        self,
        file_path: Path,
        target_loudness=-20.0,
        attack=5.0,
        release=100.0,
        threshold=-20.0,
        ratio=2.5,
    ) -> None:
        """
        Enhance audio using professional-grade processing.
        Args:
            file_path (Path): Path to the audio file
            target_loudness (float): Target loudness in dBFS (default: -20.0)
            attack (float): Compressor attack time in ms (default: 5.0)
            release (float): Compressor release time in ms (default: 100.0)
            threshold (float): Compression threshold in dBFS (default: -20.0)
            ratio (float): Compression ratio (default: 2.5)
        """
        try:
            audio = AudioSegment.from_file(str(file_path))
            enhanced = (
                audio.apply_gain(-audio.dBFS + target_loudness)
                .compress_dynamic_range(
                    threshold=threshold, ratio=ratio, attack=attack, release=release
                )
                .normalize(headroom=0.1)
            )

            # Export processed audio
            enhanced.export(
                str(file_path),
                format=file_path.suffix.lstrip("."),
                parameters=["-q:a", "2"],  # High quality encoding
            )
            print(f"Successfully enhanced audio: {file_path}")
        except Exception as e:
            print(f"Audio enhancement failed: {str(e)}")
            print("Continuing with original audio")

    def enhance_audio_minimal(
        self, file_path: Path, speed_factor: float = 1.15
    ) -> None:
        """
        Minimal processing for multi-speaker content
        Args:
            file_path (Path): Path to the audio file
            speed_factor (float): Playback speed factor (default 1.15) (original 1.0)
        """
        try:
            audio = AudioSegment.from_file(str(file_path))
            # Adjust speed without changing pitch
            audio = audio.speedup(playback_speed=speed_factor)
            # Only normalize if significant volume differences
            if abs(audio.dBFS + 18.0) > 3.0:  # +/- 3dB tolerance
                audio = audio.normalize(target_level=-18.0)

            # Export with high quality
            audio.export(
                str(file_path),
                format=file_path.suffix.lstrip("."),
                parameters=["-q:a", "2"],
            )
        except Exception as e:
            print(f"Normalization failed: {str(e)}")
            print("Continuing with original audio")


class AudioSynthesizer(AudioEnhancer):
    def merge_audio_files(self, input_dir: str, output_file: str) -> None:
        """
        Merge all audio files in the input directory sequentially and save the result.
        Args:
            input_dir (str): Path to the directory containing audio files.
            output_file (str): Path to save the merged audio file.
        """
        try:

            def natural_sort_key(filename: str) -> List[Union[int, str]]:
                return [
                    int(text) if text.isdigit() else text
                    for text in re.split(r"(\d+)", filename)
                ]

            combined = AudioSegment.empty()
            audio_files = sorted(
                [f for f in os.listdir(input_dir) if f.endswith("mp3")],
                key=natural_sort_key,
            )
            for file in audio_files:
                if file.endswith("mp3"):
                    file_path = os.path.join(input_dir, file)
                    combined += AudioSegment.from_file(file_path, format="mp3")

            combined.export(output_file, format="mp3")
            print(f"Merged audio saved to {output_file}")
        except Exception as e:
            raise Exception(f"Error merging audio files: {str(e)}")

    def enhance_audio(self, file_path: Path) -> None:
        """
        Enhanced audio processing with voice-optimized settings
        Args:
            file_path (Path): Path to the audio file
            voice_mode (bool): Use voice-optimized settings if True
        """
        # Voice-optimized settings
        super().enhance_audio(
            file_path,
            target_loudness=-18.0,  # Slightly louder for voice
            attack=10.0,  # Slower attack to preserve transients
            release=50.0,  # Faster release for natural speech
            threshold=-24.0,  # Lower threshold for voice
            ratio=2.0,  # Gentler compression for voice
        )
