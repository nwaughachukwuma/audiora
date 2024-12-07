from pydantic import BaseModel

from src.utils.audiocast_request import GenerateSourceContent
from src.utils.chat_utils import ContentCategory
from src.utils.decorators.base import use_cache_manager
from src.utils.make_seed import get_hash
from src.utils.session_manager import SessionManager


class GenerateAiSourceRequest(BaseModel):
    sessionId: str
    category: ContentCategory
    preferenceSummary: str


async def generate_ai_source(request: GenerateAiSourceRequest):
    """
    Generate ai source material based on user preferences.
    """
    preference_summary = request.preferenceSummary
    category = request.category
    session_id = request.sessionId

    params = {"sessionId": session_id, "category": category, "preference_summary": preference_summary}
    cache_key = get_hash(params, "audio_source")

    @use_cache_manager(cache_key)
    async def _handler():
        db = SessionManager(session_id, category)
        db._update_info("Generating source content...")

        generator = GenerateSourceContent(category, preference_summary)
        source_content = await generator._run()
        db._update_source(source_content)

        return source_content

    return await _handler()
