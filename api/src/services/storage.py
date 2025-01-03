import datetime
import os
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4

from google.auth import compute_engine, default
from google.auth.transport import requests
from google.cloud import storage
from pydub import AudioSegment

from src.env_var import BUCKET_NAME

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)
BLOB_BASE_URI = "audiora/assets"


def listBlobs(prefix):
    blobs = bucket.list_blobs(prefix=prefix)
    return [blob for blob in blobs]


@dataclass
class UploadItemParams:
    content_type: str
    cache_control: str = "public, max-age=31536000"
    metadata: Dict[str, Any] | None = None


class StorageManager:
    bucket_name = BUCKET_NAME

    def check_blob_exists(self, filename: str, root_path=BLOB_BASE_URI):
        """check if a file exists in the bucket"""
        blobname = f"{root_path}/{filename}"
        blobs = listBlobs(prefix=root_path)
        return any(blob.name == blobname for blob in blobs)

    def upload_to_gcs(self, item: str | Path | BytesIO, blobname: str, params: UploadItemParams):
        """upload item to GCS"""
        blob = bucket.blob(blobname)
        blob.content_type = params.content_type
        blob.cache_control = params.cache_control

        if params.metadata:
            blob.metadata = {**(blob.metadata or dict()), **params.metadata}

        if isinstance(item, Path):
            blob.upload_from_filename(str(item))
        elif isinstance(item, str):
            blob.upload_from_string(item)
        else:
            blob.upload_from_file(item)

        return f"gs://{BUCKET_NAME}/{blob.name}"

    def upload_audio_to_gcs(self, tmp_audio_path: str, filename=str(uuid4())):
        """upload audio file to GCS"""
        blobname = f"{BLOB_BASE_URI}/{filename}"
        self.upload_to_gcs(
            Path(tmp_audio_path),
            blobname,
            UploadItemParams(content_type="audio/mpeg"),
        )

        return f"gs://{BUCKET_NAME}/{blobname}"

    def upload_video_to_gcs(self, tmp_video_path: str, filename=str(uuid4())):
        """upload audio file to GCS"""
        blobname = f"{BLOB_BASE_URI}/{filename}"
        self.upload_to_gcs(
            Path(tmp_video_path),
            blobname,
            UploadItemParams(content_type="video/mp4"),
        )

        return f"gs://{BUCKET_NAME}/{blobname}"

    def download_from_gcs(self, filename: str):
        """
        Download any item on GCS to disk
        """
        blobname = f"{BLOB_BASE_URI}/{filename}"
        blob = bucket.blob(blobname)

        tmp_file_path = f"/tmp/{filename}"
        if os.path.exists(tmp_file_path):
            try:
                audio = AudioSegment.from_file(tmp_file_path)
                if audio.duration_seconds > 0:
                    return tmp_file_path
            except Exception:
                os.remove(tmp_file_path)

        blob.download_to_filename(tmp_file_path)
        return tmp_file_path

    def get_signed_url(self, blobname, expiration=datetime.timedelta(days=1)):
        """get a signed URL for a blob"""
        blob = bucket.blob(blobname)
        if not blob.exists():
            raise Exception(f"Blob {blobname} does not exist")

        if os.environ.get("ENV", "dev") == "prod":
            credentials, _ = default()
            auth_request = requests.Request()
            credentials.refresh(auth_request)

            signing_credentials = compute_engine.IDTokenCredentials(
                auth_request, "", service_account_email=credentials.service_account_email
            )

            return blob.generate_signed_url(
                version="v4",
                expiration=expiration,
                method="GET",
                credentials=signing_credentials,
            )
        else:
            return blob.generate_signed_url(
                version="v4",
                expiration=expiration,
                method="GET",
            )

    def get_gcs_url(self, filename: str):
        """get full path to a file in the bucket"""
        blobname = f"{BLOB_BASE_URI}/{filename}"
        return f"gs://{BUCKET_NAME}/{blobname}"

    def get_blob(self, blobname: str):
        """get a blob object"""
        return bucket.blob(blobname)

    def get_blobname_from_url(self, url: str):
        """get blobname from a URL"""
        return url.replace(f"gs://{self.bucket_name}/", "")
