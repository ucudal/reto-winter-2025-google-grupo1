from abc import ABC, abstractmethod
import io
import json
from google.cloud import bigquery
from typing import Dict, Any
from datetime import datetime

class IRepository(ABC):
    """
    Base repository interface for CREATE, READ, and DELETE operations.
    It defines a contract for all repository implementations.
    """

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> bool:
        """
        Inserts a new record into the repository.
        :param data: Dictionary with the data to insert.
        :return: True if the insertion was successful, False otherwise.
        """
        pass

    @abstractmethod
    def read(self, record_id: str) -> Dict[str, Any] or None:
        """
        Reads a record by its unique identifier.
        :param record_id: The ID of the record to find.
        :return: A dictionary with the record's data or None if not found.
        """
        pass

    @abstractmethod
    def update(self, record_id: str, data: Dict[str, Any]) -> bool:
        """Updates an existing record in the repository.

        :param record_id: The unique identifier of the record to update.
        :param data: A dictionary containing the fields and new values.
        :return: True if the update was successful, False otherwise.
        """
        pass

    @abstractmethod
    def delete(self, record_id: str) -> bool:
        """
        Deletes a record by its unique identifier.
        :param record_id: The ID of the record to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        pass

class UserRepository(IRepository):
    """Repository implementation for the users table in BigQuery."""

    def __init__(self, project_id: str, dataset_id: str):
        self.client = bigquery.Client(project=project_id)
        self.table_ref = f"{project_id}.{dataset_id}.users"
        self.id_column = "user_id"

    def create(self, data: Dict[str, Any]) -> bool:
        try:
            # Serializa el diccionario de Python a una cadena JSON válida
            json_data = json.dumps(data)

            # Prepara los datos en un archivo en memoria
            jsonl_data = io.StringIO(f"{json_data}\n")

            # Crea una configuración de trabajo para la carga
            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND
            )

            # Inicia el trabajo de carga
            load_job = self.client.load_table_from_file(
                jsonl_data,
                self.table_ref,
                job_config=job_config
            )

            # Espera a que el trabajo termine
            load_job.result()
            print(f"Batch load successful for: {data.get(self.id_column)}")
            return True
        except Exception as e:
            print(f"Error inserting into '{self.table_ref}': {e}")
            return False

    def update(self, record_id: str, data: Dict[str, Any]) -> bool:
        """
        This method is not required for the users table, so it returns False.
        """
        print("Warning: Update is not supported for the UserRepository.")
        return False

    def read(self, record_id: str) -> Dict[str, Any] or None:
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
        try:
            self.client.query(query, job_config=job_config).result()
            return True
        except Exception as e:
            print(f"Error deleting from 'users': {e}")
            return False


class ConversationRepository(IRepository):
    """Repository implementation for the conversations table in BigQuery."""

    def __init__(self, project_id: str, dataset_id: str):
        self.client = bigquery.Client(project=project_id)
        self.table_ref = f"{project_id}.{dataset_id}.conversations"
        self.id_column = "conversation_id"

    def create(self, data: Dict[str, Any]) -> bool:
        try:
            # Serializa el diccionario de Python a una cadena JSON válida
            json_data = json.dumps(data)

            # Prepara los datos en un archivo en memoria
            jsonl_data = io.StringIO(f"{json_data}\n")

            # Crea una configuración de trabajo para la carga
            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND
            )

            # Inicia el trabajo de carga
            load_job = self.client.load_table_from_file(
                jsonl_data,
                self.table_ref,
                job_config=job_config
            )

            # Espera a que el trabajo termine
            load_job.result()
            print(f"Batch load successful for: {data.get(self.id_column)}")
            return True
        except Exception as e:
            print(f"Error inserting into '{self.table_ref}': {e}")
            return False

    def update(self, record_id: str, data: Dict[str, Any]) -> bool:
        """
        Updates an existing conversation record.
        This is a specific update for the 'ended_at' timestamp.
        """
        try:
            # We assume 'data' contains the new timestamp for 'ended_at'
            if 'ended_at' not in data:
                print("Update failed: 'ended_at' field is missing from data.")
                return False

            ended_at_str = data['ended_at'].isoformat() if isinstance(data['ended_at'], datetime) else data['ended_at']

            # Use MERGE to update the specific record
            merge_query = f"""
                MERGE `{self.table_ref}` T
                USING (SELECT '{record_id}' as conversation_id) S
                ON T.conversation_id = S.conversation_id
                WHEN MATCHED THEN
                    UPDATE SET ended_at = TIMESTAMP('{ended_at_str}')
            """
            self.client.query(merge_query).result()
            print(f"Conversation {record_id} updated successfully with ended_at.")
            return True
        except Exception as e:
            print(f"Error updating conversation {record_id}: {e}")
            return False

    def read(self, record_id: str) -> Dict[str, Any] or None:
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
        try:
            self.client.query(query, job_config=job_config).result()
            return True
        except Exception as e:
            print(f"Error deleting from 'conversations': {e}")
            return False


class MessageRepository(IRepository):
    """Repository implementation for the messages table in BigQuery."""

    def __init__(self, project_id: str, dataset_id: str):
        self.client = bigquery.Client(project=project_id)
        self.table_ref = f"{project_id}.{dataset_id}.messages"
        self.id_column = "message_id"

    def create(self, data: Dict[str, Any]) -> bool:
        try:
            # Serializa el diccionario de Python a una cadena JSON válida
            json_data = json.dumps(data)

            # Prepara los datos en un archivo en memoria
            jsonl_data = io.StringIO(f"{json_data}\n")

            # Crea una configuración de trabajo para la carga
            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND
            )

            # Inicia el trabajo de carga
            load_job = self.client.load_table_from_file(
                jsonl_data,
                self.table_ref,
                job_config=job_config
            )

            # Espera a que el trabajo termine
            load_job.result()
            print(f"Batch load successful for: {data.get(self.id_column)}")
            return True
        except Exception as e:
            print(f"Error inserting into '{self.table_ref}': {e}")
            return False

    def update(self, record_id: str, data: Dict[str, Any]) -> bool:
        """
        This method is not required for the users table, so it returns False.
        """
        print("Warning: Update is not supported for the UserRepository.")
        return False


    def read(self, record_id: str) -> Dict[str, Any] or None:
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
        try:
            self.client.query(query, job_config=job_config).result()
            return True
        except Exception as e:
            print(f"Error deleting from 'messages': {e}")
            return False
