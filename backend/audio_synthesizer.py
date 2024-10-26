from pathlib import Path

import numpy as np
import pyttsx3
import soundfile as sf


class AudioSynthesizer:
    def __init__(self, output_dir: str = "audio_files"):
        self.engine = pyttsx3.init()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Configure voice properties
        self.engine.setProperty("rate", 150)  # Speed of speech
        self.engine.setProperty("volume", 0.9)  # Volume (0.0 to 1.0)

        # Get available voices and set a good quality one
        voices = self.engine.getProperty("voices")
        if voices:
            # Usually, the second voice is better quality
            self.engine.setProperty(
                "voice", voices[1].id if len(voices) > 1 else voices[0].id
            )

    def synthesize(self, text: str, file_id: str) -> str:
        """
        Synthesize text to speech and save as audio file

        Args:
            text (str): The text to synthesize
            file_id (str): Unique identifier for the audio file

        Returns:
            str: Path to the generated audio file
        """
        output_path = self.output_dir / f"{file_id}.mp3"

        # Save audio to file
        self.engine.save_to_file(text, str(output_path))
        self.engine.runAndWait()

        # Enhance audio quality (optional post-processing)
        self._enhance_audio(output_path)

        return str(output_path)

    def _enhance_audio(self, file_path: Path):
        """
        Apply basic audio enhancements

        Args:
            file_path (Path): Path to the audio file
        """
        try:
            # Read the audio file
            data, samplerate = sf.read(file_path)

            # Apply basic normalization
            normalized_data = data / np.max(np.abs(data))

            # Apply very slight compression
            threshold = 0.3
            ratio = 0.7
            compressed_data = np.where(
                np.abs(normalized_data) > threshold,
                threshold
                + (np.abs(normalized_data) - threshold)
                * ratio
                * np.sign(normalized_data),
                normalized_data,
            )

            # Write the enhanced audio
            sf.write(file_path, compressed_data, samplerate)

        except Exception as e:
            print(f"Warning: Audio enhancement failed: {e}")
            # Continue with original audio if enhancement fails
