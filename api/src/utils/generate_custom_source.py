from typing import Optional, cast

from fastapi import BackgroundTasks
from pydantic import BaseModel

from src.services.firestore_sdk import (
    Collection,
    DBManager,
    collections,
)
from src.utils.extract_url_content import ExtractURLContent, URLContent


class GenerateCustomSourceRequest(BaseModel):
    url: str
    sessionId: str


class GetCustomSourcesRequest(BaseModel):
    sessionId: str


class CustomSourceModel(URLContent):
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


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

    def _set_custom_source(self, data: CustomSourceModel):
        self._check_document()

        doc_ref = self._get_collection(self.collection).document(self.doc_id)
        return (
            doc_ref.collection(self.sub_collection)
            .document(data.id)
            .set({**(data.model_dump()), "created_at": self._timestamp, "updated_at": self._timestamp})
        )

    def _get_custom_source(self, source_id: str) -> CustomSourceModel:
        self._check_document()
        return (
            self._get_collection(self.collection)
            .document(self.doc_id)
            .collection(self.sub_collection)
            .document(source_id)
            .get()
        )

    def _get_custom_sources(self):
        self._check_document()

        try:
            doc_ref = self._get_collection(self.collection).document(self.doc_id)
            docs = doc_ref.collection(self.sub_collection).get()
            return [
                cast(CustomSourceModel, self._safe_to_dict(doc.to_dict()))
                for doc in docs
                if doc.exists and doc.to_dict()
            ]

        except Exception as e:
            print(f"Error getting custom sources for Session: {self.doc_id}", e)
            return []


async def generate_custom_source(request: GenerateCustomSourceRequest, background_tasks: BackgroundTasks):
    extractor = ExtractURLContent()
    page_content = await extractor._extract(request.url)

    async def save_to_firestore():
        custom_source = CustomSourceModel(**page_content.model_dump())
        manager = CustomSourceManager(request.sessionId)
        manager._set_custom_source(custom_source)

    background_tasks.add_task(save_to_firestore)
    return page_content.model_dump()
