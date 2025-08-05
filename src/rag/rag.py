from typing import cast, final
from google.cloud import bigquery
from google.genai.types import ContentEmbedding

from chat.types import Dependencies
from rag.types import DocumentFragment, RAGQuery


@final
class RAGTool:
    def __init__(self, deps: Dependencies, embedding_model: str = "models/embedding-001"):
        self._deps = deps
        self._embedding_model = embedding_model

    async def _get_embedding(self, text: str) -> ContentEmbedding | None:
        response = await self._deps.google_client.models.embed_content(
            model=self._embedding_model, contents=text, config={"task_type": "retrieval_query"}
        )
        return response.embeddings[0] if response.embeddings else None

    async def retrieve_with_vector_search(
        self, rag_query: RAGQuery
    ) -> list[tuple[DocumentFragment, float]]:
        query_embedding_obj = await self._get_embedding(rag_query.query)

        if query_embedding_obj is None:
            return []

        # The actual list of float values for the embedding
        embedding_values = query_embedding_obj.values
        env = self._deps.env

        # 1. The SQL query now uses named placeholders (@param_name) instead of f-string formatting for values.
        #    Table names are kept in the f-string as they are typically not user-controlled.
        bq_query = f"""
        SELECT base.*, distance
        FROM VECTOR_SEARCH(
            TABLE `{env.project_id}.{env.dataset}.{env.table}`, 'embedding',
            (SELECT @embedding AS embedding),
            top_k => @top_k, distance_type => 'COSINE'
        ) AS base
        WHERE 1 - distance >= @similarity_threshold
        """

        # 2. Create a JobConfig to define the parameters and their types.
        #    This is the core of preventing SQL injection.
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ArrayQueryParameter("embedding", "FLOAT64", embedding_values),
                bigquery.ScalarQueryParameter("top_k", "INT64", rag_query.top_k),
                bigquery.ScalarQueryParameter(
                    "similarity_threshold", "FLOAT64", rag_query.similarity_threshold
                ),
            ]
        )

        # 3. Pass the query and the job_config to the client.
        #    The client library will now safely handle parameter substitution.
        query_job = self._deps.bq_client.query(bq_query, job_config=job_config)
        results = query_job.result()
        documents = list[tuple[DocumentFragment, float]]()

        for row in results:
            documents.append((DocumentFragment.model_validate(row.base), cast(float, row.distance)))

        return documents
