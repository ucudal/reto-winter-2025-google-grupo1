from functools import cache

from google import genai
from google.cloud import bigquery


@cache
def create_bq_client(project_id: str):
    return bigquery.Client(project_id)

@cache
def create_google_client(api_key: str):
    return genai.Client(api_key=api_key)
