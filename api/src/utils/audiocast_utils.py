from typing import TypedDict

from pydantic import BaseModel

from src.utils.chat_utils import ContentCategory


class GenerateAudioCastRequest(BaseModel):
    sessionId: str
    summary: str
    category: ContentCategory


class GenerateAudioCastResponse(BaseModel):
    created_at: str | None


class GenerateAudiocastDict(TypedDict):
    url: str
    script: str
    source_content: str
    created_at: str | None
