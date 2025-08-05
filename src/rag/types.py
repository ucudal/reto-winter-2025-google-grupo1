from datetime import datetime
from pydantic import BaseModel, Field


class DocumentFragment(BaseModel):
    """A fragment of a document. When using its information, always cite its id as a source."""

    document_id: str
    fragment_text: str
    created_at: datetime


class RAGQuery(BaseModel):
    """A query to search in our knowledge database (RAG). It contains information about Ithaka."""

    query: str
    top_k: int = Field(default=3, description="Número de documentos más relevantes a recuperar")
    similarity_threshold: float = Field(default=0.3, description="Umbral de similitud mínimo")
