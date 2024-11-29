from fastapi import HTTPException

from src.services.storage import StorageManager

from .decorators import process_time
from .session_manager import SessionManager


@process_time()
def get_audiocast(session_id: str):
    """
    Get audiocast based on session_id
    """
    try:
        exists = StorageManager().check_blob_exists(session_id)
        if not exists:
            raise
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Failed to get audiocast for session_id: {session_id}",
        )

    session_data = SessionManager.data(session_id)
    if not session_data:
        raise HTTPException(
            status_code=404,
            detail=f"Audiocast not found for session_id: {session_id}",
        )

    if session_data.status != "completed":
        SessionManager._update_status(session_id, "completed")

    return session_data.__dict__
