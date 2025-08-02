from functools import cache
import os
from typing import Literal
from uuid import uuid4
from pydantic import BaseModel, Field

EnvironmentKind = Literal["prod", "dev"]

class Environment(BaseModel, frozen=True):
    google_cloud_api_key: str = Field(alias="GOOGLE_CLOUD_API_KEY")
    environment: EnvironmentKind =  Field(default="dev", alias="ENVIRONMENT")
    user_id: str = Field(default=str(uuid4()), alias="USER_ID")


# This is the only global state, but that's intentional.
@cache
def env() -> Environment:
    return Environment.model_validate(dict(os.environ))
