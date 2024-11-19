from datetime import datetime

from fastapi import BackgroundTasks, HTTPException

from src.services.storage import StorageManager
from src.utils.audio_manager import AudioManager, AudioManagerConfig
from src.utils.audiocast_script_maker import AudioScriptMaker
from src.utils.audiocast_utils import (
    GenerateAudioCastRequest,
    GenerateAudioCastResponse,
)
from src.utils.generate_audiocast_source import GenerateAudiocastSource, generate_audiocast_source
from src.utils.session_manager import SessionManager
from src.utils.waveform_utils import WaveformUtils


async def generate_audiocast(request: GenerateAudioCastRequest, background_tasks: BackgroundTasks):
    """## Generate audiocast based on a summary of user's request

    ### Steps:
    1. Generate source content
    2. Generate audio script
    3. Generate audio
    4a. Store audio
    4b. Store the audio waveform on GCS
    5. Update session
    """
    summary = request.summary
    category = request.category
    session_id = request.sessionId

    source_content = await generate_audiocast_source(
        GenerateAudiocastSource(
            sessionId=session_id,
            category=category,
            preferenceSummary=summary,
        ),
        background_tasks,
    )

    db = SessionManager(session_id, category)

    def update_session_info(info: str):
        background_tasks.add_task(db._update_info, info)

    if not source_content:
        raise HTTPException(status_code=500, detail="Failed to generate source content")

    # Generate audio script
    update_session_info("Generating audio script...")
    script_maker = AudioScriptMaker(category, source_content)
    audio_script = script_maker.create(provider="gemini")

    if not audio_script:
        raise HTTPException(status_code=500, detail="Failed to generate audio script")

    # Generate audio
    update_session_info("Generating audio...")
    audio_manager = AudioManager(custom_config=AudioManagerConfig(tts_provider="openai"))
    audio_path = await audio_manager.generate_speech(audio_script)

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

    session_data = SessionManager.data(session_id)
    if not session_data:
        raise HTTPException(
            status_code=404,
            detail=f"Failed to get audiocast from the DB for session_id: {session_id}",
        )

    title = session_data.metadata.title if session_data.metadata and session_data.metadata.title else "Untitled"

    return GenerateAudioCastResponse(
        script=audio_script,
        source_content=source_content,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        chats=session_data.chats,
        title=title,
        category=session_data.category,
    )
