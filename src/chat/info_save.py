import mimetypes
from uuid import uuid4
from typing import Union
from google.cloud import storage
from pydantic_ai.models import BinaryContent
from pydantic_ai.models._openai_types import ImageUrl, AudioUrl, FileUrl, VideoUrl


async def upload(file: BinaryContent, userId: str, conversationId: str) -> Union[ImageUrl, AudioUrl, FileUrl, VideoUrl]:
    """
    Sube un archivo a Google Cloud Storage y retorna la URL correspondiente.
    
    Args:
        file: Contenido binario del archivo
        userId: ID del usuario
        conversationId: ID de la conversación
        
    Returns:
        URL del archivo subido (ImageUrl, AudioUrl, FileUrl, o VideoUrl)
    """
    try:
        # Inicializar cliente de Cloud Storage
        client = storage.Client()
        bucket_name = "reto_winter_equipo1"  # Tu bucket correcto
        bucket = client.bucket(bucket_name)
        
        # Detectar tipo de archivo basado en el contenido
        mime_type = file.media_type if hasattr(file, 'media_type') else None
        if not mime_type:
            # Intentar detectar por extensión si está disponible
            mime_type = "application/octet-stream"
        
        # Determinar extensión del archivo
        extension = get_file_extension(mime_type)
        
        # Generar nombre único del archivo
        file_id = str(uuid4())
        blob_name = f"uploads/{userId}/{conversationId}/{file_id}{extension}"
        
        # Crear blob y subir archivo
        blob = bucket.blob(blob_name)
        blob.upload_from_string(
            file.data if hasattr(file, 'data') else file,
            content_type=mime_type
        )
        
        # Hacer el archivo público (opcional, dependiendo de tus necesidades)
        blob.make_public()
        
        # Obtener URL pública
        public_url = blob.public_url
        
        # Retornar el tipo de URL apropiado basado en el tipo de archivo
        return create_typed_url(public_url, mime_type)
        
    except Exception as e:
        raise Exception(f"Error subiendo archivo a Cloud Storage: {str(e)}")


def get_file_extension(mime_type: str) -> str:
    """
    Obtiene la extensión del archivo basada en el tipo MIME.
    
    Args:
        mime_type: Tipo MIME del archivo
        
    Returns:
        Extensión del archivo con punto incluido
    """
    extensions = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/webp': '.webp',
        'audio/mpeg': '.mp3',
        'audio/wav': '.wav',
        'audio/ogg': '.ogg',
        'video/mp4': '.mp4',
        'video/webm': '.webm',
        'video/quicktime': '.mov',
        'application/pdf': '.pdf',
        'text/plain': '.txt',
        'application/json': '.json',
        'application/xml': '.xml',
    }
    
    return extensions.get(mime_type, '.bin')


def create_typed_url(url: str, mime_type: str) -> Union[ImageUrl, AudioUrl, FileUrl, VideoUrl]:
    """
    Crea el tipo de URL apropiado basado en el tipo MIME.
    
    Args:
        url: URL del archivo
        mime_type: Tipo MIME del archivo
        
    Returns:
        URL tipada apropiada
    """
    if mime_type.startswith('image/'):
        return ImageUrl(url=url)
    elif mime_type.startswith('audio/'):
        return AudioUrl(url=url)
    elif mime_type.startswith('video/'):
        return VideoUrl(url=url)
    else:
        return FileUrl(url=url)
