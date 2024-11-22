from datetime import datetime

from fastapi import BackgroundTasks, HTTPException

from src.services.storage import StorageManager
from src.utils.audio_manager import AudioManager, AudioManagerConfig
from src.utils.audiocast_script_maker import AudioScriptMaker
from src.utils.audiocast_utils import (
    GenerateAudioCastRequest,
    GenerateAudioCastResponse,
)
from src.utils.chat_utils import ContentCategory
from src.utils.custom_sources.base_utils import CustomSourceManager
from src.utils.generate_audiocast_source import GenerateAudiocastSource, generate_audiocast_source
from src.utils.session_manager import SessionManager
from src.utils.waveform_utils import WaveformUtils


def compile_custom_sources(session_id: str):
    sources = CustomSourceManager(session_id)._get_custom_sources()
    return "\n\n".join([str(source) for source in sources if source["content"]])


def post_generate_audio(
    session_id: str,
    category: ContentCategory,
    audio_path: str,
    audio_script: str,
):
    try:
        # Store audio
        storage_manager = StorageManager()
        storage_manager.upload_audio_to_gcs(audio_path, session_id)

        # Update session metadata
        db = SessionManager(session_id, category)
        db._update_transcript(audio_script)

        # Generate and save audio waveform as mp4
        waveform_utils = WaveformUtils(session_id, audio_path)
        waveform_utils.run_all()
    except Exception as e:
        print(f"Error in generate_audiocast background_tasks: {str(e)}")


async def generate_audiocast(request: GenerateAudioCastRequest, background_tasks: BackgroundTasks):
    """## Generate audiocast based on a summary of user's request

    ### Steps:
    1. Generate source content
    2. Generate audio script
    3. Generate audio
    4. a) Store audio. b) Store the audio waveform on GCS
    5. Update session
    """
    summary = request.summary
    category = request.category
    session_id = request.sessionId

    db = SessionManager(session_id, category)

    def update_session_info(info: str):
        background_tasks.add_task(db._update_info, info)

    session_data = SessionManager.data(session_id)
    source_content = session_data.metadata.source if session_data and session_data.metadata else None

    if not source_content:
        update_session_info("Generating source content...")
        source_content = await generate_audiocast_source(
            GenerateAudiocastSource(
                sessionId=session_id,
                category=category,
                preferenceSummary=summary,
            ),
            background_tasks,
        )

    if not source_content:
        raise HTTPException(status_code=500, detail="Failed to generate source content")

    # get custom sources
    update_session_info("Checking for custom sources...")
    compiled_custom_sources = compile_custom_sources(session_id)

    # Generate audio script
    update_session_info("Generating audio script...")
    script_maker = AudioScriptMaker(category, source_content, compiled_custom_sources)
    audio_script = script_maker.create(provider="gemini")

    if not audio_script:
        raise HTTPException(status_code=500, detail="Failed to generate audio script")

    # Generate audio
    update_session_info("Generating audio...")
    audio_manager = AudioManager(custom_config=AudioManagerConfig(tts_provider="openai"))
    audio_path = await audio_manager.generate_speech(audio_script)

    background_tasks.add_task(
        post_generate_audio,
        session_id,
        category,
        audio_path,
        audio_script,
    )

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
