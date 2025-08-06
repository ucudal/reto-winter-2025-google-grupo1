import io
import json
from google.cloud import bigquery
from pydantic import BaseModel

class UserModel(BaseModel):
    user_id: str
    ...


class UserRepository:
    """Repository implementation for the users table in BigQuery."""

    def __init__(self, client: bigquery.Client, project_id: str, dataset_id: str):
        self.client: bigquery.Client = client
        self.table_ref: str = f"{project_id}.{dataset_id}.users"
        self.id_column: str = "user_id"

    def create(self, data: UserModel) -> bool:
        # Serializa el diccionario de Python a una cadena JSON válida
        json_data = data.model_dump_json()

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
        _ = load_job.result()
        print(f"Batch load successful for: {data.user_id}")
        return True

    def read(self, record_id: str) -> UserModel | None:
        query = f"SELECT * FROM `{self.table_ref}` WHERE {self.id_column} = @record_id LIMIT 1"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("record_id", "STRING", record_id)]
        )
        query_job = self.client.query(query, job_config=job_config)
        results = list(query_job.result())

        return UserModel.model_validate(dict(results[0].items())) if results else None

    def delete(self, record_id: str) -> bool:
        query = f"DELETE FROM `{self.table_ref}` WHERE {self.id_column} = @record_id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("record_id", "STRING", record_id)]
        )
        _ = self.client.query(query, job_config=job_config).result()
        return True
