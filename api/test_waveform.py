#!/usr/bin/env python3
"""
Test script to verify SeeWav waveform generation with different quality settings
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.utils.waveform_utils import WaveformUtils


def test_waveform_generation():
    """Test waveform generation with different quality settings"""
    # Use the previously generated test audio file
    test_audio = "/tmp/test_openai_tts.mp3"

    if not os.path.exists(test_audio):
        print("❌ Test audio file not found. Please run TTS test first.")
        return False

    print("Testing SeeWav waveform generation...")

    # Test different quality settings
    for quality in ("medium", "high"):
        try:
            print(f"\n🔄 Testing {quality} quality...")
            waveform_utils = WaveformUtils("test_session", test_audio)

            # Get output path
            output_path = Path(f"/tmp/test_waveform_{quality}.mp4")

            # Generate waveform
            result = waveform_utils.generate_waveform_video(output_path, quality=quality)

            if result and result.exists():
                file_size = result.stat().st_size
                print(f"✅ {quality.capitalize()} quality waveform generated: {result}")
                print(f"   File size: {file_size:,} bytes")
            else:
                print(f"❌ Failed to generate {quality} quality waveform")
                return False

        except Exception as e:
            print(f"❌ Error generating {quality} quality waveform: {str(e)}")
            return False

    print("\n✅ All waveform tests passed!")
    return True


if __name__ == "__main__":
    success = test_waveform_generation()
    sys.exit(0 if success else 1)
