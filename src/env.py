from functools import cache
import json
import os
from typing import Literal, Union
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator

EnvironmentTag = Literal["prod", "dev"]
MemoryTag = Literal["local", "bigquery"]
AnswerTag = Literal["text", "audio"]

class Environment(BaseModel, frozen=True):
    google_cloud_api_key: str = Field(alias="GOOGLE_CLOUD_API_KEY")
    environment: EnvironmentTag = Field(default="dev", alias="ENVIRONMENT")
    user_id: str = Field(default_factory=lambda: str(uuid4()), alias="USER_ID")
    conversation_id: str = Field(default_factory=lambda: str(uuid4()), alias="CONVERSATION_ID")
    project_id: str = Field(alias='PROJECT_ID')
    bucket_name: str = Field(alias='BUCKET_NAME')
    dataset: str = Field(alias='DATASET')
    table: str = Field(alias='TABLE')
    memory: MemoryTag = Field(default="local", alias="MEMORY")
    answer: AnswerTag = Field(default="text", alias="ANSWER")
    credentials: Union[dict, str] = Field(default_factory=dict, alias="CREDENTIALS")
    
    @field_validator('credentials', mode='before')
    @classmethod
    def parse_credentials(cls, v):
        """Parsea las credenciales si están en formato string JSON"""
        if isinstance(v, str) and v.strip():
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return v
        return v


# This is the only global state, but that's intentional.
@cache
def env() -> Environment:
    return Environment.model_validate(dict(os.environ))
