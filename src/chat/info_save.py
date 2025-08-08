# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false

import asyncio
from uuid import uuid4
from google.cloud import storage
from pydantic_ai import AudioUrl, BinaryContent, DocumentUrl, ImageUrl, VideoUrl

StoredUrl = ImageUrl | AudioUrl | DocumentUrl | VideoUrl


async def upload(file: BinaryContent) -> StoredUrl:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _sync_upload, file)

def _sync_upload(file: BinaryContent) -> StoredUrl:
    client = storage.Client()
    bucket_name = "reto_winter_equipo1"
    bucket = client.bucket(bucket_name)

    mime_type = file.media_type
    extension = get_file_extension(mime_type)
    file_id = str(uuid4())
    blob_name = f"uploads/{file_id}{extension}"

    blob = bucket.blob(blob_name)
    blob.upload_from_string(file.data, content_type=mime_type)
    blob.make_public()

    public_url = blob.public_url
    return tag_url(public_url, mime_type)


def get_file_extension(mime_type: str) -> str:
    """
    Obtiene la extensión del archivo basada en el tipo MIME.

    Args:
        mime_type: Tipo MIME del archivo

    Returns:
        Extensión del archivo con punto incluido
    """
    extensions = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
        "audio/mpeg": ".mp3",
        "audio/wav": ".wav",
        "audio/ogg": ".ogg",
        "video/mp4": ".mp4",
        "video/webm": ".webm",
        "video/quicktime": ".mov",
        "application/pdf": ".pdf",
        "text/plain": ".txt",
        "application/json": ".json",
        "application/xml": ".xml",
    }

    return extensions.get(mime_type, ".bin")


def tag_url(url: str, mime_type: str) -> StoredUrl:
    """
    Crea el tipo de URL apropiado basado en el tipo MIME.

    Args:
        url: URL del archivo
        mime_type: Tipo MIME del archivo

    Returns:
        URL tipada apropiada
    """
    if mime_type.startswith("image/"):
        return ImageUrl(url=url, media_type=mime_type)
    elif mime_type.startswith("audio/"):
        return AudioUrl(url=url, media_type=mime_type)
    elif mime_type.startswith("video/"):
        return VideoUrl(url=url, media_type=mime_type)
    else:
        return DocumentUrl(url=url, media_type=mime_type)
