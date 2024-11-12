from datetime import datetime

from fastapi import HTTPException

from src.utils.generate_audiocast import GenerateAudioCastResponse
from src.utils.session_manager import SessionManager


def get_audiocast(session_id: str):
    """
    Get audiocast based on session id
    """
    session_data = SessionManager.data(session_id)
    if not session_data:
        raise HTTPException(
            status_code=404,
            detail=f"Audiocast not found for session_id: {session_id}",
        )

    metadata = session_data.metadata
    source = metadata.source if metadata else ""
    transcript = metadata.transcript if metadata else ""
    title = metadata.title if metadata and metadata.title else "Untitled"

    created_at = None
    if session_data.created_at:
        created_at = datetime.fromisoformat(session_data.created_at).strftime("%Y-%m-%d %H:%M")

    return GenerateAudioCastResponse(
        script=transcript,
        source_content=source,
        created_at=created_at,
        chats=session_data.chats,
        title=title,
    )
