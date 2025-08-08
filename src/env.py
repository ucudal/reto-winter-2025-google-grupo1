from functools import cache
import os
from typing import Literal
from uuid import uuid4
from pydantic import BaseModel, Field

EnvironmentTag = Literal["prod", "dev"]
MemoryTag = Literal["local", "bigquery"]
AnswerTag = Literal["text", "audio"]

class Environment(BaseModel, frozen=True):
    google_cloud_api_key: str = Field(alias="GOOGLE_CLOUD_API_KEY")
    environment: EnvironmentTag =  Field(default="dev", alias="ENVIRONMENT")
    user_id: str = Field(default_factory=lambda: str(uuid4()), alias="USER_ID")
    conversation_id: str = Field(default_factory=lambda: str(uuid4()), alias="CONVERSATION_ID")
    project_id: str = Field(alias='PROJECT_ID')
    bucket_name: str = Field(alias='BUCKET_NAME')
    dataset: str = Field(alias='DATASET')
    table: str = Field(alias='TABLE')
    memory: MemoryTag = Field(default="local", alias="MEMORY")
    answer: AnswerTag = Field(default="text", alias="ANSWER")


# This is the only global state, but that's intentional.
@cache
def env() -> Environment:
    return Environment.model_validate(dict(os.environ))
