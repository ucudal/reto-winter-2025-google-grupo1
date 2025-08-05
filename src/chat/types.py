from google.cloud import bigquery
from google.genai.client import AsyncClient
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from env import Environment

UserId = str

@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Dependencies:
    env: Environment
    google_client: AsyncClient
    bq_client: bigquery.Client
