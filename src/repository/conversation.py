from datetime import datetime
import io
import json
from google.cloud import bigquery
from pydantic import BaseModel


class ConversationModel(BaseModel):
    conversation_id: str
    user_id: str
    started_at: datetime | None
    ended_at: datetime | None


class ConversationRepository:
    """Repository implementation for the conversations table in BigQuery."""

    def __init__(self, client: bigquery.Client, project_id: str, dataset_id: str):
        self.client: bigquery.Client = client
        self.table_ref: str = f"{project_id}.{dataset_id}.users"
        self.id_column: str = "conversation_id"

    def create(self, data: ConversationModel) -> bool:
        try:
            # Serializa el diccionario de Python a una cadena JSON válida
            json_data = data.model_dump_json()

            # Prepara los datos en un archivo en memoria
            jsonl_data = io.StringIO(f"{json_data}\n")

            # Crea una configuración de trabajo para la carga
            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            )

            # Inicia el trabajo de carga
            load_job = self.client.load_table_from_file(
                jsonl_data, self.table_ref, job_config=job_config
            )

            # Espera a que el trabajo termine
            _ = load_job.result()
            print(f"Batch load successful for: {data.conversation_id}")
            return True
        except Exception as e:
            print(f"Error inserting into '{self.table_ref}': {e}")
            return False

    def update(self, record_id: str, ended_at: datetime) -> bool:
        """
        Updates an existing conversation record.
        This is a specific update for the 'ended_at' timestamp.
        """
        try:
            # Use MERGE to update the specific record
            merge_query = f"""
                MERGE `{self.table_ref}` T
                USING (SELECT '{record_id}' as conversation_id) S
                ON T.conversation_id = S.conversation_id
                WHEN MATCHED THEN
                    UPDATE SET ended_at = TIMESTAMP('{ended_at.isoformat:)}')
            """
            _ = self.client.query(merge_query).result()
            print(f"Conversation {record_id} updated successfully with ended_at.")
            return True
        except Exception as e:
            print(f"Error updating conversation {record_id}: {e}")
            return False

    def read(self, record_id: str) -> ConversationModel | None:
        query = f"SELECT * FROM `{self.table_ref}` WHERE {self.id_column} = @record_id LIMIT 1"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("record_id", "STRING", record_id)]
        )
        query_job = self.client.query(query, job_config=job_config)
        results = list(query_job.result())

        return ConversationModel.model_validate(dict(results[0].items())) if results else None

    def delete(self, record_id: str) -> bool:
        query = f"DELETE FROM `{self.table_ref}` WHERE {self.id_column} = @record_id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("record_id", "STRING", record_id)]
        )
        _ = self.client.query(query, job_config=job_config).result()
        return True
