from datetime import datetime

from fastapi import BackgroundTasks, HTTPException

from services.storage import StorageManager
from src.utils.audiocast_request import AudioScriptMaker, generate_source_content
from utils_pkg.audio_manager import AudioManager, AudioManagerConfig
from utils_pkg.audiocast_utils import (
    GenerateAudioCastRequest,
    GenerateAudioCastResponse,
)
from utils_pkg.session_manager import SessionManager
from utils_pkg.waveform_utils import WaveformUtils


async def generate_audiocast(
    request: GenerateAudioCastRequest, background_tasks: BackgroundTasks
):
    """## Generate audiocast based on a summary of user's request

    ### Steps:
    1. Generate source content
    2. Generate audio script
    3. Generate audio
    4a. Store audio
    4b. TODO: Store the audio waveform on GCS
    5. Update session
    """
    summary = request.summary
    category = request.category
    session_id = request.sessionId

    db = SessionManager(session_id)

    def update_session_info(info: str):
        background_tasks.add_task(db._update_info, info)

    update_session_info("Generating source content...")

    source_content = generate_source_content(category, summary)
    if not source_content:
        raise HTTPException(status_code=500, detail="Failed to generate source content")

    # Generate audio script
    update_session_info("Generating audio script...")
    audio_script_maker = AudioScriptMaker(category, source_content)
    audio_script = audio_script_maker.create(provider="anthropic")
    if not audio_script:
        raise HTTPException(status_code=500, detail="Failed to generate audio script")

    # Generate audio
    update_session_info("Generating audio...")
    audio_path = await AudioManager(
        custom_config=AudioManagerConfig(tts_provider="elevenlabs")
    ).generate_speech(audio_script)

    def _run_on_background():
        try:
            # Store audio
            storage_manager = StorageManager()
            storage_manager.upload_audio_to_gcs(audio_path, session_id)

            # Update session metadata
            db._update_source(source_content)
            db._update_transcript(audio_script)
            # TODO: add one to update title

            # Generate and save audio waveform as mp4
            waveform_utils = WaveformUtils(session_id, audio_path)
            waveform_utils.run_all()
        except Exception as e:
            print(f"Error in generate_audiocast background_tasks: {str(e)}")

    background_tasks.add_task(_run_on_background)

    return GenerateAudioCastResponse(
        url=audio_path,
        script=audio_script,
        source_content=source_content,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
