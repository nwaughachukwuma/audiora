def streamline_audio_script_prompt(instruction: str, audio_script: str):
    """
    Streamline the audio script to align with the specified TTS requirements.
    """
    return f"""Your task is to streamline an auto-generated audio script to match the specified TTS requirements. 
    
    TTS Requirements: {instruction}
    Generated Audio Script: {audio_script}

    1. Keep a very high fidelity of the structure and content of the generated audio script.
    2. Carefully remove any unnecessary information.
    3. Ensure the script is optimized for TTS delivery.
        - Ensure all open tags are closed.
        - Ensure all SSML tags are properly formatted.
        - Ensure all speaker tags are properly formatted.
    4. Ensure the audio script strictly aligns with the requirements.
    5. You're not to add any new information to or change the nature of the script.
    """
