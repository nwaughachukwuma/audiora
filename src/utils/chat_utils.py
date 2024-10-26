from typing import Dict, List, Literal

from pydantic import BaseModel

ContentType = Literal["story", "podcast", "sermon", "science"]

content_types: List[ContentType] = ["story", "podcast", "sermon", "science"]

content_examples: Dict[ContentType, str] = {
    "story": "Tell me a story about a magical kingdom with dragons and wizards.",
    "podcast": "Create a podcast about the history of space exploration.",
    "sermon": "Write a sermon about finding peace in times of trouble.",
    "science": "Explain the concept of black holes in simple terms.",
}


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class SessionChatRequest(BaseModel):
    content_type: ContentType
    message: ChatMessage
