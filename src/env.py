from functools import cache
import os
from pydantic import BaseModel, Field


class Environment(BaseModel, frozen=True):
    google_cloud_api_key: str = Field(alias='GOOGLE_CLOUD_API_KEY')
    project_id: str = Field(alias='PROJECT_ID')
    bucket_name: str = Field(alias='BUCKET_NAME')
    dataset: str = Field(alias='DATASET')
    table: str = Field(alias='TABLE')


@cache
def env() -> Environment:
    return Environment.model_validate(dict(os.environ))
