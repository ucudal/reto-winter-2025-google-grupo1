from functools import cache
import os
from typing import Literal
from pydantic import BaseModel, Field

EnvironmentKind = Literal["prod", "dev"]

class Environment(BaseModel, frozen=True):
    google_cloud_api_key: str = Field(alias="GOOGLE_CLOUD_API_KEY")
    environment: EnvironmentKind = "dev"


# This is the only global state, but that's intentional.
@cache
def env() -> Environment:
    return Environment.model_validate(dict(os.environ))
