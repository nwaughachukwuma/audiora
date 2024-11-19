from fastapi import BackgroundTasks
from pydantic import BaseModel

from src.utils.audiocast_request import GenerateSourceContent
from src.utils.chat_utils import ContentCategory
from src.utils.decorators import use_cache_manager
from src.utils.make_seed import get_hash
from src.utils.session_manager import SessionManager


class GenerateAudiocastSource(BaseModel):
    sessionId: str
    category: ContentCategory
    preferenceSummary: str


async def generate_audiocast_source(request: GenerateAudiocastSource, background_tasks: BackgroundTasks):
    """
    Generate audiocast source material based on user preferences.
    """
    preference_summary = request.preferenceSummary
    category = request.category
    session_id = request.sessionId

    params = {"sessionId": session_id, "category": category, "preference_summary": preference_summary}
    cache_key = get_hash(params, "audio_source")

    @use_cache_manager(cache_key)
    async def _handler():
        def update_session_info(info: str):
            db = SessionManager(session_id, category)
            background_tasks.add_task(db._update_info, info)

        update_session_info("Generating source content...")
        source_content_generator = GenerateSourceContent(category, preference_summary)
        source_content = await source_content_generator._run()

        return source_content

    return await _handler()
