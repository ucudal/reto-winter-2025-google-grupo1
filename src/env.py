from functools import cache
import os
from pydantic import BaseModel, Field


class Environment(BaseModel, frozen=True):
    google_cloud_api_key: str = Field(alias='GOOGLE_CLOUD_API_KEY')


@cache
def env() -> Environment:
    return Environment.model_validate(dict(os.environ))
