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
    "podcast": "Podcast exploring the intersection of ancient philosophy and AI",
    "sermon": "Sermon connecting the teachings of Augustine with modern digital ethics",
    "audiodrama": "Reimagining of Homer's Odyssey set in a cyberpunk future",
    "lecture": "Lecture comparing Shakespeare's influence on modern social media",
    "commentary": "Commentary on how Classical music influences contemporary electronic genres",
    "voicenote": "Personal reflection on reading Plato's Republic in today's political climate",
    "interview": "Interview with an archaeologist using AI to uncover ancient Roman artifacts",
    "soundbite": "Quick take on how ancient Greek democracy shapes modern blockchain governance",
}

category_qualifiers: Dict[ContentCategory, str] = {
    "podcast": "an engaging, illustrative, and informative podcast",
    "sermon": "an inspiring, reflective, and thought-provoking sermon",
    "audiodrama": "an immersive, dramatic, and emotionally resonant audiodrama",
    "lecture": "an educational, structured, and comprehensive lecture",
    "commentary": "a analytical, insightful, and critical commentary",
    "voicenote": "a personal, authentic, and concise voicenote",
    "interview": "a conversational, revealing, and dynamic interview",
    "soundbite": "an impactful, memorable, and informative soundbite",
}


class SessionChatItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: Literal["user", "assistant"]
    content: str


class SessionChatRequest(BaseModel):
    contentCategory: ContentCategory
    chatItem: SessionChatItem
