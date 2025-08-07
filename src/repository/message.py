from __future__ import annotations

import json
import uuid
from datetime import datetime
import io
from typing import Literal, Dict, Any
from google.cloud import bigquery
from pydantic import BaseModel, Field

from chat.memory import MessageContent, MessagesContentTypeAdapter

class MessageModel(BaseModel):
    message_id: str
    conversation_id: str
    sender: Literal["user", "assistant"]
    # A singular message may contain multiple parts (text, quotes, files)
    message_text: list[MessageContent]
    # I wonder how precise this is, since I will be creating both the user
    # prompt and and model question at the same time.
    timestamp: datetime


class MessageRepository:
    """Repository implementation for the messages table in BigQuery."""

    def __init__(self, client: bigquery.Client, project_id: str, dataset_id: str):
        self.client: bigquery.Client = client
        self.table_ref: str = f"{project_id}.{dataset_id}.messages"
        self.id_column: str = "conversation_id"
        self.id_column = "message_id"

    def create(self, conversation_id: str, message_json: Dict[str, Any]) -> str | None:
        """Crea un nuevo mensaje con un ID autonumérico, manejando errores.

        :param conversation_id: El ID de la conversación a la que pertenece el mensaje.
        :param message_json: Un diccionario con el contenido del mensaje.
        :return: El ID del nuevo mensaje si es exitoso, o None si falla.
        """
        try:
            new_id = str(uuid.uuid4())
            data = MessageModel(
                message_id=new_id,
                conversation_id=conversation_id,
                timestamp=datetime.utcnow(),
                message_text=[MessageContent(**message_json)]
            )
            json_data = data.model_dump_json()

            jsonl_data = io.StringIO(f"{json_data}\n")

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
        except Exception as e:
            # Captura cualquier excepción que ocurra durante la carga
            print(f"Error creating message: {e}")
            return None


    def read(self, record_id: str) -> dict[str, object] | None:
        query = f"SELECT * FROM `{self.table_ref}` WHERE {self.id_column} = @record_id LIMIT 1"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("record_id", "STRING", record_id)]
        )
        query_job = self.client.query(query, job_config=job_config)
        results = list(query_job.result())

        return dict(results[0].items()) if results else None

    def delete(self, record_id: str) -> bool:
        query = f"DELETE FROM `{self.table_ref}` WHERE {self.id_column} = @record_id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("record_id", "STRING", record_id)]
        )

        _ = self.client.query(query, job_config=job_config).result()
        return True
