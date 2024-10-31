from dataclasses import dataclass
from typing import Dict, List, Optional, cast

from src.services.firestore_sdk import (
    Collection,
    DBManager,
    arrayRemove,
    arrayUnion,
    collections,
)
from src.utils.chat_utils import SessionChatMessage


@dataclass
class ChatMetadata:
    source: str
    transcript: str


@dataclass
class SessionModel:
    id: str
    chats: List[SessionChatMessage]
    metadata: Optional[ChatMetadata]
    created_at: Optional[str] = None


class SessionManager(DBManager):
    collection: Collection = collections["audiora_sessions"]

    def __init__(self, session_id: str):
        super().__init__(scope="ChatManager")

        self.doc_id = session_id
        session_doc = self._get_document(self.collection, self.doc_id)
        # if the collection does not exist, create it
        if not session_doc.exists:
            payload = SessionModel(id=self.doc_id, chats=[], metadata=None)
            self._set_document(self.collection, self.doc_id, payload.__dict__)

    def _update(self, data: Dict):
        return self._update_document(self.collection, self.doc_id, data)

    def data(self) -> SessionModel | None:
        doc = self._get_document(self.collection, self.doc_id)

        data = doc.to_dict()
        if not doc.exists or not data:
            return None

        metadata = data["metadata"] or {}

        return SessionModel(
            id=data["id"],
            chats=data["chats"],
            metadata=ChatMetadata(
                source=metadata.get("source", ""),
                transcript=metadata.get("transcript", ""),
            ),
            created_at=str(data["created_at"]),
        )

    def _update_source(self, source: str):
        return self._update({"metadata.source": source})

    def _update_transcript(self, transcript: str):
        return self._update({"metadata.transcript": transcript})

    def _add_chat(self, chat: SessionChatMessage):
        return self._update_document(
            self.collection, self.doc_id, {"chats": arrayUnion([chat.__dict__])}
        )

    def _delete_chat(self, chat_id: str):
        doc = self._get_document(self.collection, self.doc_id)
        if not doc.exists:
            return

        chat_to_remove = [chat for chat in doc.get("chats") if chat.id == chat_id]
        self._update_document(
            self.collection,
            self.doc_id,
            {"chats": arrayRemove([chat_to_remove.__dict__])},
        )

    def _get_chat(self, chat_id: str) -> SessionChatMessage | None:
        doc = self._get_document(self.collection, self.doc_id)
        if not doc.exists:
            return None

        item = [chat for chat in doc.get("chats") if chat.id == chat_id][0]
        if item:
            return SessionChatMessage(
                content=item["content"],
                id=item["id"],
                role=item["role"],
            )

    def _get_chats(self) -> List[SessionChatMessage]:
        doc = self._get_document(self.collection, self.doc_id)
        if not doc.exists:
            return []

        chats = cast(Dict, doc.get("chats"))
        return [
            SessionChatMessage(
                content=chat["content"],
                id=chat["id"],
                role=chat["role"],
            )
            for chat in chats
        ]
