from functools import cache
import os
from typing import Literal
from uuid import uuid4
from google.oauth2 import service_account
from pydantic import BaseModel, Field, TypeAdapter, field_validator

EnvironmentTag = Literal["prod", "dev"]
MemoryTag = Literal["local", "bigquery"]
AnswerTag = Literal["text", "audio"]


class Environment(BaseModel, frozen=True, arbitrary_types_allowed=True):
    google_cloud_api_key: str = Field(alias="GOOGLE_CLOUD_API_KEY")
    environment: EnvironmentTag = Field(default="dev", alias="ENVIRONMENT")
    user_id: str = Field(default_factory=lambda: str(uuid4()), alias="USER_ID")
    conversation_id: str = Field(default_factory=lambda: str(uuid4()), alias="CONVERSATION_ID")
    project_id: str = Field(alias="PROJECT_ID")
    bucket_name: str = Field(alias="BUCKET_NAME")
    dataset: str = Field(alias="DATASET")
    table: str = Field(alias="TABLE")
    memory: MemoryTag = Field(default="local", alias="MEMORY")
    answer: AnswerTag = Field(default="text", alias="ANSWER")
    credentials: service_account.Credentials = Field(alias="CREDENTIALS")

    @field_validator("credentials", mode="before")
    @classmethod
    def parse_credentials(cls, val: object) -> service_account.Credentials:
        assert isinstance(val, str)

        parsed = TypeAdapter(dict[str, object]).validate_json(val)
        output = service_account.Credentials.from_service_account_info(parsed)  # pyright: ignore[reportUnknownMemberType]
        return output


# This is the only global state, but that's intentional.
@cache
def env() -> Environment:
    return Environment.model_validate(dict(os.environ))
