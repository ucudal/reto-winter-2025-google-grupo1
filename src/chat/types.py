from typing import Literal
from google.cloud import bigquery
from google.genai.client import AsyncClient
from pydantic import BaseModel, ConfigDict
from pydantic.dataclasses import dataclass
from pydantic_ai import BinaryContent

from env import Environment

UserId = str

class Citation(BaseModel):
    tag: Literal["citation"] = "citation"
    text: str
    author: str


class Link(BaseModel):
    tag: Literal["link"] = "link"
    text: str
    author: str
    link: str

type Quote = Citation | Link


class TextAnswer(BaseModel):
    kind: Literal["text"] = "text"
    text: str

AnswerPart = TextAnswer | BinaryContent

class Answer(BaseModel):
    content: AnswerPart
    quotes: list[Quote] = []

@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Dependencies:
    env: Environment
    google_client: AsyncClient
    bq_client: bigquery.Client
    quotes: list[Quote]
