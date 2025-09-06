#!/usr/bin/env python3
"""
Simple test script to verify OpenAI TTS implementation
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.utils.generate_speech_utils import GenerateSpeech, SpeechJob


def test_openai_tts():
    """Test OpenAI TTS functionality"""
    # Create a simple speech job
    job = SpeechJob(
        content="Hello! This is a test of the OpenAI TTS system. It should work perfectly.",
        voice="nova",
        output_file="/tmp/test_openai_tts.mp3",
        tag="test",
        index=1,
    )

    try:
        # Create speech generator and run
        generator = GenerateSpeech()
        result = generator.run(job)

        if result and os.path.exists(result):
            print(f"✅ Success! Audio file created: {result}")
            file_size = os.path.getsize(result)
            print(f"File size: {file_size} bytes")
            return True
        else:
            print("❌ Failed to generate audio file")
            return False
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return False
    finally:
        if os.path.exists(job.output_file):
            os.remove(job.output_file)


if __name__ == "__main__":
    print("Testing OpenAI TTS implementation...")
    success = test_openai_tts()
    sys.exit(0 if success else 1)
