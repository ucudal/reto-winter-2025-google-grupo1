from __future__ import annotations
import uuid
from datetime import datetime, date
import io
from typing import Literal, Tuple

from google.cloud import bigquery
from pydantic import BaseModel

from message import MessageModel
from forms.test_form import IthakaEvaluationSupportForm, Evaluator, UcuCommunityMember, Faculty, Stage, ProfileType,SupportType, Mentor, FollowUpPerson


class FormModel(IthakaEvaluationSupportForm):
    form_id: str
    message_id: str


class FormRepository:
    """Repository implementation for the froms table in BigQuery."""

    def __init__(self, client: bigquery.Client, project_id: str, dataset_id: str):
        self.client: bigquery.Client = client
        self.table_ref: str = f"{project_id}.{dataset_id}.forms"
        self.id_column: str = "form_id"
        self.participant_column: str = "name"

    def create(self,
               message_id: str,
               name: str,
               first_question: Literal["Evaluación primaria del Sponsor", "Comité de evaluación"] | None,
               date_of_completion: date,
               evaluators: Tuple[Evaluator | None, Evaluator | None],
               idea: str,
               sponsor: str,
               ucu_community_members: Tuple[UcuCommunityMember, UcuCommunityMember | None],
               linked_faculty: Tuple[Faculty | None, Faculty | None],
               stage: Tuple[Stage, Stage | None],
               profile_type: list[ProfileType],
               potential_support: list[SupportType],
               specific_mentor: list[Mentor],
               follow_up_personnel: Tuple[FollowUpPerson, FollowUpPerson | None],
               internal_comments: str,
               message_for_applicant: str) -> str | None:
        """Crea una nueva conversación con un ID autonumérico
        :return: El ID del form si es exitosa, o None si falla.
        """
        new_id = str(uuid.uuid4())
        data = FormModel(form_id=new_id,
                         message_id=message_id,
                         name=name,
                         first_question=first_question,
                         date_of_completion=date_of_completion,
                         evaluators=evaluators,
                         idea=idea,
                         sponsor=sponsor,
                         ucu_community_members=ucu_community_members,
                         linked_faculty=linked_faculty,
                         stage=stage,
                         profile_type=profile_type,
                         potential_support=potential_support,
                         specific_mentor=specific_mentor,
                         follow_up_personnel=follow_up_personnel,
                         internal_comments=internal_comments,
                         message_for_applicant=message_for_applicant)
        json_data = data.model_dump_json()

        jsonl_data = io.BytesIO(f"{json_data}\n".encode('utf-8'))

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
        print(f"Formulario creado con ID: {new_id}")
        return new_id

    def read(self, name: str) -> FormModel | None:
        query = (f"""
                    SELECT *
                    FROM `{self.table_ref}`
                    WHERE `{self.participant_column}` = @name LIMIT 1""")

        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("name", "STRING", name)]
        )
        query_job = self.client.query(query, job_config=job_config)
        results = list(query_job.result())

        return FormModel.model_validate(dict(results[0].items())) if results else None

    def delete(self, record_id: str) -> bool:
        query = f"DELETE FROM `{self.table_ref}` WHERE {self.id_column} = @record_id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("record_id", "STRING", record_id)]
        )
        _ = self.client.query(query, job_config=job_config).result()
        return True
