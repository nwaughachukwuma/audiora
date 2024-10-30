import re
from dataclasses import dataclass
from io import BytesIO
from typing import Any, Dict
from uuid import uuid4

from google.cloud import storage

from src.env_var import BUCKET_NAME

# Instantiates a client
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)


def listBlobs(prefix):
    blobs = bucket.list_blobs(prefix=prefix)
    return [blob for blob in blobs]


def download_audio_file(root_cloud_path: str, tmp_path: str):
    """download the video file from the bucket"""
    blobs = listBlobs(prefix=root_cloud_path)
    pattern = re.compile("audio/mpeg|audio/mp3|audio/wav|audio/ogg|audio/aac")
    audio_blobs = [blob for blob in blobs if bool(pattern.match(blob.content_type))]

    if not len(audio_blobs):
        return None

    audio_file = audio_blobs[0]
    audio_file.download_to_filename(f"{tmp_path}")

    return tmp_path


def check_file_exists(root_path: str, filename: str):
    """check if a file exists in the bucket"""
    blobname = f"{root_path}/{filename}"
    blobs = listBlobs(prefix=root_path)
    return any(blob.name == blobname for blob in blobs)


@dataclass
class UploadItemParams:
    content_type: str
    cache_control: str = "public, max-age=31536000"
    metadata: Dict[str, Any] | None = None


def upload_string_to_gcs(content: str, blobname: str, params: UploadItemParams):
    """upload string content to GCS"""
    blob = bucket.blob(blobname)
    blob.content_type = "text/plain"
    blob.cache_control = params.content_type

    if params.metadata:
        blob.metadata = {**(blob.metadata or dict()), **params.metadata}

    blob.upload_from_string(content)

    return f"gs://{BUCKET_NAME}/{blob.name}"


def upload_file_to_gcs(tmp_path: str, blobname: str, params: UploadItemParams):
    """upload file to GCS"""
    blob = bucket.blob(blobname)
    blob.content_type = params.content_type
    blob.cache_control = params.cache_control

    if params.metadata:
        blob.metadata = {**(blob.metadata or dict()), **params.metadata}

    blob.upload_from_filename(tmp_path)

    return f"gs://{BUCKET_NAME}/{blob.name}"


def upload_bytes_to_gcs(bytes: BytesIO, blobname: str, params: UploadItemParams):
    """upload bytes to GCS"""
    blob = bucket.blob(blobname)
    blob.content_type = params.content_type
    blob.cache_control = params.cache_control

    if params.metadata:
        blob.metadata = {**(blob.metadata or dict()), **params.metadata}

    blob.upload_from_file(bytes)

    return f"gs://{BUCKET_NAME}/{blobname}"


def download_file_from_gcs(blobname: str):
    """
    Download any item on GCS to disk
    """
    blob = bucket.blob(blobname)
    tmp_file_path = f"/tmp/{str(uuid4())}"
    blob.download_to_filename(tmp_file_path)

    return tmp_file_path
