from typing import List, TypedDict

from pydantic import BaseModel

from src.utils.chat_utils import ContentCategory, SessionChatItem


class GenerateAudioCastRequest(BaseModel):
    sessionId: str
    summary: str
    category: ContentCategory


class GenerateAudioCastResponse(BaseModel):
    script: str
    source_content: str
    chats: List[SessionChatItem]
    category: ContentCategory
    title: str | None
    created_at: str | None


class GenerateAudiocastDict(TypedDict):
    url: str
    script: str
    source_content: str
    created_at: str | None
