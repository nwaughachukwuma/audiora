from typing import Literal

from pydantic import BaseModel

ContentType = Literal["story", "podcast", "sermon", "science"]


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class SessionChatRequest(BaseModel):
    content_type: ContentType
    message: ChatMessage
