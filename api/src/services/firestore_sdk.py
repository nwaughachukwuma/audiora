from datetime import datetime
from typing import Dict, Literal

from firebase_admin.firestore import client, firestore

firestore_client = client()
server_timestamp = firestore.SERVER_TIMESTAMP
increment = firestore.Increment
arrayUnion = firestore.ArrayUnion
arrayRemove = firestore.ArrayRemove


Collection = Literal["audiora_sessions", "audiora_audiocasts"]

collections: Dict[Collection, Collection] = {
    "audiora_sessions": "audiora_sessions",
    "audiora_audiocasts": "audiora_audiocasts",
}


class DBManager:
    @property
    def _timestamp(self):
        return server_timestamp

    def _get_collection(self, collection: Collection):
        return firestore_client.collection(collections[collection])

    def _create_document(self, collection: Collection, data: Dict):
        return self._get_collection(collection).add(
            {**data, "created_at": self._timestamp, "updated_at": self._timestamp}
        )

    def _set_document(self, collection: Collection, doc_id: str, data: Dict):
        return (
            self._get_collection(collection)
            .document(doc_id)
            .set({**data, "created_at": self._timestamp, "updated_at": self._timestamp})
        )

    def _update_document(self, collection: Collection, doc_id: str, data: Dict):
        return self._get_collection(collection).document(doc_id).update({**data, "updated_at": self._timestamp})

    def _delete_document(self, collection: Collection, doc_id: str):
        return self._get_collection(collection).document(doc_id).delete()

    def _get_document(self, collection: Collection, doc_id: str):
        return self._get_collection(collection).document(doc_id).get()

    def _get_documents(self, collection: Collection):
        return self._get_collection(collection).stream()

    @classmethod
    def _safe_to_dict(cls, data: dict):
        """
        safely parse firestore data by converting convert all timestamp to string
        """

        def _safe_to_str(value: dict | str | datetime):
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d %H:%M:%S")
            return value

        return {k: _safe_to_str(v) for k, v in data.items()}
