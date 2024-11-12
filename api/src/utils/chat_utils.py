import uuid
from typing import Dict, List, Literal

from pydantic import BaseModel, Field

ContentCategory = Literal[
    "podcast",
    "soundbite",
    "sermon",
    "audiodrama",
    "commentary",
    "lecture",
    "voicenote",
    "interview",
]

content_categories: List[ContentCategory] = [
    "podcast",
    "soundbite",
    "sermon",
    "audiodrama",
    "commentary",
    "lecture",
    "voicenote",
    "interview",
]

content_examples: Dict[ContentCategory, str] = {
    "podcast": "Create a podcast exploring the intersection of ancient philosophy and artificial intelligence.",
    "sermon": "Write a sermon connecting the teachings of Augustine with modern digital ethics.",
    "audiodrama": "A reimagining of Homer's Odyssey set in a cyberpunk future.",
    "lecture": "A lecture comparing Shakespeare's influence on modern social media communication.",
    "commentary": "A commentary on how Classical music influences contemporary electronic genres.",
    "voicenote": "A personal reflection on reading Plato's Republic in today's political climate.",
    "interview": "An interview with an archaeologist using AI to uncover ancient Roman artifacts.",
    "soundbite": "A quick take on how ancient Greek democracy shapes modern blockchain governance.",
}

category_qualifiers: Dict[ContentCategory, str] = {
    "podcast": "an engaging, illustrative, and informative podcast",
    "sermon": "an inspiring, reflective, and thought-provoking sermon",
    "audiodrama": "an immersive, dramatic, and emotionally resonant audiodrama",
    "lecture": "an educational, structured, and comprehensive lecture",
    "commentary": "a analytical, insightful, and critical commentary",
    "voicenote": "a personal, authentic, and concise voicenote",
    "interview": "a conversational, revealing, and dynamic interview",
    "soundbite": "an impactful, memorable, and succinct soundbite",
}


class SessionChatItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: Literal["user", "assistant"]
    content: str


class SessionChatRequest(BaseModel):
    contentCategory: ContentCategory
    chatItem: SessionChatItem
