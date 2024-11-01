import os
import subprocess


def create_video_from_audio(audio_path: str, image_path: str, output_path: str):
    """Create a video with audio and spectrogram overlay."""
    cmd = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-i",
        image_path,
        "-i",
        audio_path,
        "-c:v",
        "libx264",
        "-tune",
        "stillimage",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-pix_fmt",
        "yuv420p",
        "-shortest",
        output_path,
    ]

    try:
        subprocess.run(cmd, check=True)
        os.remove(image_path)  # Clean up temporary spectrogram
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during video creation: {str(e)}")
        return False
    except Exception as e:
        print(f"Error during video creation: {str(e)}")
