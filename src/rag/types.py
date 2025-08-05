from datetime import datetime
from pydantic import BaseModel, Field


class DocumentFragment(BaseModel):
    """A fragment of a document. When using its information, always cite its id as a source."""

    document_id: str
    fragment_text: str
    created_at: datetime


class RAGQuery(BaseModel):
    """A query to search in the knowledge database (RAG)."""

    query: str
    top_k: int = Field(default=3, description="Number of most relevant documents to retrieve")
    similarity_threshold: float = Field(default=0.3, description="Minimum similarity threshold")
