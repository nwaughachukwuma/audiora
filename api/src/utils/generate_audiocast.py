import asyncio
import os

from fastapi import BackgroundTasks, HTTPException

from src.env_var import PROD_ENV
from src.services.storage import StorageManager

from .audio_manager import AudioManager, AudioManagerConfig
from .audiocast_script_maker import AudioScriptMaker
from .audiocast_utils import GenerateAudioCastRequest
from .chat_utils import ContentCategory
from .custom_sources.base_utils import CustomSourceManager
from .generate_audiocast_source import GenerateAiSourceRequest, generate_ai_source
from .session_manager import SessionManager
from .waveform_utils import WaveformUtils


class GenerateAudiocastException(HTTPException):
    name = "GenerateAudiocastException"

    def __init__(self, detail: str, session_id: str, status_code=500):
        self.detail = detail
        self.status_code = status_code
        self.session_id = session_id


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
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)


async def generate_audiocast(request: GenerateAudioCastRequest, background_tasks: BackgroundTasks):
    """## Generate audiocast based on a summary of user's request"""
    summary = request.summary
    category = request.category
    session_id = request.sessionId

    db = SessionManager(session_id, category)
    session_data = SessionManager.data(session_id)

    if not session_data:
        raise GenerateAudiocastException(
            status_code=404, detail=f"Audiocast data not found for session_id: {session_id}", session_id=session_id
        )

    if session_data.status == "completed":
        return "Audiocast already generated!"
    elif session_data.status == "generating":
        print(f"Queueing the current audio generation request>>>>\n\nSessionId: {session_id}")

        async def retry_generation():
            await asyncio.sleep(10)
            try:
                await generate_audiocast(request, background_tasks)
            except Exception as e:
                print(f"Retry failed for session {session_id}: {str(e)}")
                SessionManager._update_status(session_id, "failed")

        background_tasks.add_task(retry_generation)
        return "Audiocast generation in progress. Please wait..."

    db._update({"status": "generating"})

    def update_session_info(info: str):
        db._update_info(info)

    ai_source = session_data.metadata.source if session_data and session_data.metadata else None

    if not ai_source:
        update_session_info("Generating source content...")
        ai_source = await generate_ai_source(
            GenerateAiSourceRequest(
                sessionId=session_id,
                category=category,
                preferenceSummary=summary,
            ),
        )

    if not ai_source:
        raise GenerateAudiocastException(
            status_code=500, detail="Failed to generate source material", session_id=session_id
        )

    # get custom sources
    update_session_info("Checking for custom sources...")
    compiled_custom_sources = compile_custom_sources(session_id)

    # Generate audio script
    update_session_info("Generating audio script...")
    script_maker = AudioScriptMaker(category, ai_source, compiled_custom_sources)
    audio_script = script_maker.create(provider="gemini")

    if not audio_script:
        raise GenerateAudiocastException(
            status_code=500, detail="Failed to generate audio script", session_id=session_id
        )

    # Generate audio
    update_session_info("Generating audio...")

    tts_provider = "elevenlabs" if PROD_ENV else "openai"
    audio_manager = AudioManager(custom_config=AudioManagerConfig(tts_provider=tts_provider))
    audio_path = await audio_manager.generate_speech(audio_script)

    background_tasks.add_task(
        post_generate_audio,
        session_id,
        category,
        audio_path,
        audio_script,
    )
    db._update({"status": "completed"})

    return "Audiocast generated successfully!"
