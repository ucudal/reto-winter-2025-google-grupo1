"""
Módulo de herramientas para el proyecto.

Incluye herramientas RAG (Retrieval-Augmented Generation) que utilizan
embeddings de Google y Gemini para generar respuestas basadas en documentos.
"""

from .tool_with_RAG import (
    RAGTool,
    Document,
    RAGQuery,
    RAGResponse,
    query_rag_with_bigquery,
    ask_question,
)

__all__ = [
    "RAGTool",
    "Document", 
    "RAGQuery",
    "RAGResponse",
    "query_rag_with_bigquery",
    "ask_question",
]
