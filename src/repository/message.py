from __future__ import annotations
from collections.abc import Sequence
import uuid
from datetime import datetime, timezone
import io
from google.cloud import bigquery
from pydantic_ai.messages import ModelMessage

from repository.types import MessageModel, SenderType

class MessageRepository:
    """Repository implementation for the messages table in BigQuery."""

    def __init__(self, client: bigquery.Client, project_id: str, dataset_id: str):
        self.client: bigquery.Client = client
        self.table_ref: str = f"{project_id}.{dataset_id}.messages"
        self.id_column: str = "message_id"

    def create(self, conversation_id: str, sender: SenderType , content: Sequence[ModelMessage]) -> str:
        """Crea un nuevo mensaje con un ID autonumérico, manejando errores.

        :param conversation_id: El ID de la conversación a la que pertenece el mensaje.
        :param message_json: Un diccionario con el contenido del mensaje.
        :return: El ID del nuevo mensaje si es exitoso, o None si falla.
        """
        new_id = str(uuid.uuid4())
        data = MessageModel(
            message_id=new_id,
            conversation_id=conversation_id,
            sender=sender,
            timestamp=datetime.now(timezone.utc),
            message_text=list(content),
        )
        json_data = data.model_dump_json()

        jsonl_data = io.BytesIO(f"{json_data}\n".encode())

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        )

        load_job = self.client.load_table_from_file(
            jsonl_data,
            self.table_ref,
            job_config=job_config
        )

        _ = load_job.result()
        print(f"Message created successfully with ID: {new_id}")
        return new_id

    def read(self, record_id: str) -> MessageModel | None:
        query = f"SELECT * FROM `{self.table_ref}` WHERE {self.id_column} = @record_id LIMIT 1"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("record_id", "STRING", record_id)]
        )
        query_job = self.client.query(query, job_config=job_config)
        results = list(query_job.result())

        return MessageModel.model_validate(dict(results[0].items())) if results else None

    def delete(self, record_id: str) -> bool:
        query = f"DELETE FROM `{self.table_ref}` WHERE {self.id_column} = @record_id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("record_id", "STRING", record_id)]
        )

        _ = self.client.query(query, job_config=job_config).result()
        return True
