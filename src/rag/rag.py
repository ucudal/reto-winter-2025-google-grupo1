from typing import cast, final
from google.genai.types import ContentEmbedding

from chat.types import Dependencies
from rag.types import DocumentFragment, RAGQuery


@final
class RAGTool:
    def __init__(self, deps: Dependencies, embedding_model: str = "models/embedding-001"):
        self._deps = deps
        self._embedding_model = embedding_model

    async def _get_embedding(self, text: str) -> list[ContentEmbedding]:
        response = await self._deps.google_client.models.embed_content(
            model=self._embedding_model, contents=text, config={"task_type": "retrieval_query"}
        )
        return response.embeddings or []

    async def retrieve_with_vector_search(
        self, rag_query: RAGQuery
    ) -> list[tuple[DocumentFragment, float]]:
        query_embeddings = await self._get_embedding(rag_query.query)
        embedding = query_embeddings[0].values
        env = self._deps.env
        bq_query = f"""
        SELECT base.*, distance
        FROM VECTOR_SEARCH(
                TABLE `{env.project_id}.{env.dataset}.{env.table}`, 'embedding',
                (SELECT {embedding} AS embedding),
                top_k => {rag_query.top_k}, distance_type => 'COSINE'
            ) AS base
        WHERE 1 - distance >= {rag_query.similarity_threshold}
        """

        query_job = self._deps.bq_client.query(bq_query)
        results = query_job.result()
        documents = list[tuple[DocumentFragment, float]]()

        for row in results:
            documents.append((DocumentFragment.model_validate(row.base), cast(float, row.distance)))

        return documents
