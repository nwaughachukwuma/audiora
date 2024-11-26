from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, cast

from src.services.firestore_sdk import (
    Collection,
    DBManager,
    arrayRemove,
    arrayUnion,
    collections,
)
from src.utils.chat_utils import ContentCategory, SessionChatItem


@dataclass
class ChatMetadata:
    source: str
    transcript: str
    info: Optional[str] = None
    title: Optional[str] = None


@dataclass
class SessionModel:
    id: str
    category: ContentCategory
    chats: List[SessionChatItem]
    metadata: Optional[ChatMetadata]
    created_at: Optional[str] = None
    completed: Optional[bool] = None


class SessionManager(DBManager):
    collection: Collection = collections["audiora_sessions"]
    category: ContentCategory

    def __init__(self, session_id: str, category: ContentCategory):
        super().__init__()

        self.doc_id = session_id
        self.category = category
        self._init_document()

    def _init_document(self):
        """if the collection does not exist, create it"""
        try:
            session_doc = self._get_document(self.collection, self.doc_id)
        except Exception:
            session_doc = None

        if not session_doc or not session_doc.exists:
            payload = SessionModel(id=self.doc_id, chats=[], metadata=None, category=self.category)
            self._set_document(self.collection, self.doc_id, payload.__dict__)

    def _update(self, data: Dict):
        return self._update_document(self.collection, self.doc_id, data)

    @classmethod
    def data(cls, doc_id: str) -> SessionModel | None:
        """Get session data"""
        doc = DBManager()._get_document(collections["audiora_sessions"], doc_id)

        data = doc.to_dict()
        if not doc.exists or not data:
            return None

        metadata = data["metadata"] or {}

        return SessionModel(
            id=data["id"],
            # Fallback to "podcast" for previously created sessions.
            category=data.get("category", "podcast"),
            chats=data["chats"],
            metadata=ChatMetadata(
                source=metadata.get("source", ""),
                transcript=metadata.get("transcript", ""),
                info=metadata.get("info"),
                title=metadata.get("title"),
            ),
            created_at=str(data["created_at"]),
        )

    def _update_source(self, source: str):
        return self._update({"metadata.source": source})

    def _update_transcript(self, transcript: str):
        return self._update({"metadata.transcript": transcript})

    def _update_info(self, info: str):
        return self._update({"metadata.info": info})

    def _update_title(self, title: str):
        return self._update({"metadata.title": title})

    def _add_chat(self, chat: SessionChatItem):
        return self._update_document(self.collection, self.doc_id, {"chats": arrayUnion([chat.__dict__])})

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

    def _get_chat(self, chat_id: str) -> SessionChatItem | None:
        doc = self._get_document(self.collection, self.doc_id)
        if not doc.exists:
            return None

        item = [chat for chat in doc.get("chats") if chat.id == chat_id][0]
        if item:
            return SessionChatItem(
                content=item["content"],
                id=item["id"],
                role=item["role"],
            )

    def _get_chats(self) -> List[SessionChatItem]:
        doc = self._get_document(self.collection, self.doc_id)
        if not doc.exists:
            return []

        chats = cast(Dict, doc.get("chats"))
        return [
            SessionChatItem(
                id=chat["id"],
                content=chat["content"],
                role=chat["role"],
            )
            for chat in chats
        ]

    def subscribe_to_metadata_info(self, callback: Callable):
        """Subscribe to metadata.info"""
        doc_ref = self._get_collection(self.collection).document(self.doc_id)

        def on_snapshot(doc_snapshot, _changes, _read_time):
            for doc in doc_snapshot:
                if doc.exists and doc.id == self.doc_id:
                    data = doc.to_dict()
                    info = (data.get("metadata", {}) or {}).get("info")
                    callback(info)

        return doc_ref.on_snapshot(on_snapshot)
