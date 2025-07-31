from functools import cache
import os
from typing import ClassVar
from pydantic import BaseModel, ConfigDict

class Environment(BaseModel, frozen=True):
    google_cloud_api_key: str

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

@cache
def env() -> Environment:
    return Environment.model_validate(dict(os.environ))
