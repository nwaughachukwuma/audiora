from datetime import datetime

from fastapi import HTTPException

from services.storage import StorageManager
from src.utils.generate_audiocast import (
    GenerateAudioCastResponse,
)
from shared_utils_pkg.session_manager import SessionManager


def get_audiocast(session_id: str):
    """
    Get audiocast based on session id
    """
    storage_manager = StorageManager()
    filepath = storage_manager.download_from_gcs(session_id)

    session_data = SessionManager(session_id).data()
    if not session_data:
        raise HTTPException(
            status_code=404,
            detail=f"Audiocast not found for session_id: {session_id}",
        )

    metadata = session_data.metadata
    source = metadata.source if metadata else ""
    transcript = metadata.transcript if metadata else ""

    created_at = None
    if session_data.created_at:
        created_at = datetime.fromisoformat(session_data.created_at).strftime(
            "%Y-%m-%d %H:%M"
        )

    return GenerateAudioCastResponse(
        url=filepath,
        script=transcript,
        source_content=source,
        created_at=created_at,
    )
