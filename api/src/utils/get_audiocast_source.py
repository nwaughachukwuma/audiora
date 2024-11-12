from fastapi import BackgroundTasks
from pydantic import BaseModel

from src.utils.audiocast_request import generate_source_content
from src.utils.chat_utils import ContentCategory
from src.utils.decorators import use_cache_manager
from src.utils.make_seed import get_hash
from src.utils.session_manager import SessionManager


class GetAudiocastSourceModel(BaseModel):
    sessionId: str
    category: ContentCategory
    summary: str


async def get_audiocast_source(request: GetAudiocastSourceModel, background_tasks: BackgroundTasks):
    """
    Generate audiocast based on a summary of user's request
    """
    summary = request.summary
    category = request.category
    session_id = request.sessionId

    params = {"sessionId": session_id, "category": category, "summary": summary}
    cache_key = get_hash(params, "audio_source")

    @use_cache_manager(cache_key)
    async def _handler():
        def update_session_info(info: str):
            db = SessionManager(session_id, category)
            background_tasks.add_task(db._update_info, info)

        update_session_info("Generating source content...")
        source_content = generate_source_content(category, summary)
        return source_content

    return await _handler()
