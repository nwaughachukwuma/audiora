from typing import Literal, Optional, TypedDict, cast

from google.cloud.firestore_v1 import DocumentReference
from pydantic import BaseModel

from src.services.firestore_sdk import (
    Collection,
    DBManager,
    collections,
)


class SourceContent(BaseModel):
    id: str
    content: str
    content_type: str
    metadata: dict = {}
    title: Optional[str] = None

    def __str__(self):
        result = f"Content: {self.content}"
        if self.title:
            return f"Title: {self.title}\n{result}"
        return result


class CustomSourceModel(SourceContent):
    source_type: Literal["link", "copy/paste", "file_upload"]
    url: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class SourceContentDict(TypedDict):
    id: str
    content: str
    content_type: str
    metadata: dict
    title: Optional[str]


class CustomSourceModelDict(SourceContentDict):
    source_type: Literal["link", "copy/paste", "file_upload"]
    url: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]


class CustomSourceManager(DBManager):
    collection: Collection = collections["audiora_sessions"]
    sub_collection = "custom_sources"

    def __init__(self, session_id: str):
        super().__init__()
        self.doc_id = session_id

    def _check_document(self):
        """if the collection does not exist, create it"""
        doc = self._get_document(self.collection, self.doc_id)
        if not doc.exists:
            raise Exception("Session not found")
        return doc

    def _get_doc_ref(self, source_id: str) -> DocumentReference:
        self._check_document()
        return (
            self._get_collection(self.collection)
            .document(self.doc_id)
            .collection(self.sub_collection)
            .document(source_id)
        )

    def _set_custom_source(self, data: CustomSourceModel):
        return self._get_doc_ref(data.id).set(
            {
                **(data.model_dump()),
                "created_at": self._timestamp,
                "updated_at": self._timestamp,
            }
        )

    def _get_custom_source(self, source_id: str) -> CustomSourceModel | None:
        doc = self._get_doc_ref(source_id).get()
        data = doc.to_dict()
        if doc.exists and data:
            return cast(CustomSourceModel, self._safe_to_dict(data))

    def _get_custom_sources(self) -> list[CustomSourceModelDict]:
        self._check_document()

        try:
            session_ref = self._get_collection(self.collection).document(self.doc_id)
            docs = session_ref.collection(self.sub_collection).get()
            return [
                cast(CustomSourceModelDict, self._safe_to_dict(doc.to_dict()))
                for doc in docs
                if doc.exists and doc.to_dict()
            ]

        except Exception as e:
            print(f"Error getting custom sources for Session: {self.doc_id}", e)
            return []

    def _delete_custom_source(self, source_id: str):
        return self._get_doc_ref(source_id).delete()

    def _get_custom_source_by_url(self, url: str):
        self._check_document()
        try:
            session_ref = self._get_collection(self.collection).document(self.doc_id)
            docs = session_ref.collection(self.sub_collection).where("url", "==", url).get()
            for doc in docs:
                if doc.exists:
                    return cast(CustomSourceModel, self._safe_to_dict(doc.to_dict()))
        except Exception as e:
            print(f"Error getting custom sources for Session: {self.doc_id}", e)
        return None
