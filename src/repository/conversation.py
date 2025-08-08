# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
from __future__ import annotations
import uuid
from datetime import datetime, timezone
import io
from google.cloud import bigquery

from repository.types import ConversationCreationModel, ConversationModel, MessageModel


class ConversationRepository:
    """Repository implementation for the conversations table in BigQuery."""

    def __init__(self, client: bigquery.Client, project_id: str, dataset_id: str):
        self.client: bigquery.Client = client
        self.table_ref: str = f"{project_id}.{dataset_id}.conversations"
        self.table_child_ref: str = f"{project_id}.{dataset_id}.messages"
        self.id_column: str = "conversation_id"

    def create(self, user_id: str, /, *, conversation_id: str | None) -> str:
        """Crea una nueva conversación con un ID autonumérico

        :param user_id: El ID del usuario asociado a la conversación.
        :return: El ID de la nueva conversación si es exitosa, o None si falla.
        """
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())

        data = ConversationCreationModel(
            conversation_id=conversation_id, user_id=user_id, started_at=datetime.now(timezone.utc)
        )
        json_data = data.model_dump_json()


        jsonl_data = io.StringIO(f"{json_data}\n")

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )

        load_job = self.client.load_table_from_file(
            jsonl_data, # pyright: ignore[reportArgumentType]
            self.table_ref,
            job_config=job_config
        )

        # Espera a que el trabajo de carga termine.
        _ = load_job.result()
        print(f"Conversation created successfully with ID: {conversation_id}")
        return conversation_id

    def read(self, record_id: str) -> ConversationModel | None:
        query = f"""
                    SELECT 
                        t1.conversation_id,
                        t1.user_id,
                        t1.started_at,
                        t2.message_id,
                        t2.sender,
                        t2.message_text,
                        t2.timestamp AS message_timestamp
                    FROM `{self.table_ref}` AS t1
                    JOIN `{self.table_child_ref}` AS t2
                    ON t1.conversation_id = t2.conversation_id
                    WHERE t1.conversation_id = @record_id 
                    ORDER BY t2.timestamp ASC"""

        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("record_id", "STRING", record_id)]
        )
        query_job = self.client.query(query, job_config=job_config)
        results = query_job.result()

        if not results.total_rows:
            return None

        first_row = next(results)

        conversation_data = {
            "conversation_id": first_row.conversation_id,
            "user_id": first_row.user_id,
            "started_at": first_row.started_at,
            "messages": [],
        }

        query_job = self.client.query(query, job_config=job_config)
        for row in query_job.result():
            if row.message_id:
                message_data = {
                    "message_id": row.message_id,
                    "conversation_id": row.conversation_id,
                    "sender": row.sender,
                    "message_text": (row.message_text),
                    "timestamp": row.message_timestamp,
                }
                validated_message = MessageModel.model_validate(message_data).model_dump()
                _ = conversation_data["messages"].append(validated_message)

        return ConversationModel.model_validate(conversation_data)

    def delete(self, record_id: str) -> bool:
        query = f"DELETE FROM `{self.table_ref}` WHERE {self.id_column} = @record_id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("record_id", "STRING", record_id)]
        )
        _ = self.client.query(query, job_config=job_config).result()
        return True
