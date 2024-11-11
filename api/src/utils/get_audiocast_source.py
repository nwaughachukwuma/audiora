from fastapi import BackgroundTasks
from pydantic import BaseModel

from src.utils.audiocast_request import generate_source_content
from src.utils.chat_utils import ContentCategory
from src.utils.session_manager import SessionManager


class GetAudiocastSourceModel(BaseModel):
    sessionId: str
    category: ContentCategory
    summary: str


def get_audiocast_source(request: GetAudiocastSourceModel, background_tasks: BackgroundTasks):
    """## Generate audiocast based on a summary of user's request

    ### Steps:
    1. Generate source content
    """
    summary = request.summary
    category = request.category
    session_id = request.sessionId

    db = SessionManager(session_id)

    def update_session_info(info: str):
        background_tasks.add_task(db._update_info, info)

    update_session_info("Generating source content...")

    source_content = generate_source_content(category, summary)
    return source_content
