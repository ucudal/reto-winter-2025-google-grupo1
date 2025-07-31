from functools import cache
import os
from typing import ClassVar
from pydantic import BaseModel, ConfigDict


class Environment(BaseModel, frozen=True):
    google_cloud_api_key: str = Field(alias='GOOGLE_CLOUD_API_KEY')


@cache
def env() -> Environment:
    return Environment.model_validate(dict(os.environ))
