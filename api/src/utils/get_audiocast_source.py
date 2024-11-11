from fastapi import BackgroundTasks
from pydantic import BaseModel

from src.utils.audiocast_request import generate_source_content
from src.utils.cache_manager import ONE_MONTH, cache_manager
from src.utils.chat_utils import ContentCategory
from src.utils.make_seed import get_hash
from src.utils.session_manager import SessionManager


class GetAudiocastSourceModel(BaseModel):
    sessionId: str
    category: ContentCategory
    summary: str


async def get_audiocast_source(request: GetAudiocastSourceModel, background_tasks: BackgroundTasks):
    """## Generate audiocast based on a summary of user's request

    ### Steps:
    1. Generate source content
    """
    summary = request.summary
    category = request.category
    session_id = request.sessionId

    params = {"sessionId": session_id, "category": category, "summary": summary}
    cache_key = get_hash(params, "audio_source")
    cache = await cache_manager(cache_key)

    if cache:
        cached_value = cache.get("cached_value")
        if cached_value:
            return cached_value

    db = SessionManager(session_id)

    def update_session_info(info: str):
        background_tasks.add_task(db._update_info, info)

    update_session_info("Generating source content...")

    source_content = generate_source_content(category, summary)

    async def save_to_cache(content: str):
        if cache:
            redis = cache.get("redis")
            await redis.set(cache_key, content, ex=ONE_MONTH)

    if source_content:
        background_tasks.add_task(save_to_cache, source_content)

    return source_content
