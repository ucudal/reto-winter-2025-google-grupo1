from typing import Literal
from google.cloud import bigquery
from google.genai.client import AsyncClient
from pydantic import BaseModel, ConfigDict, TypeAdapter
from pydantic.dataclasses import dataclass
from pydantic_ai.messages import ModelMessage

from chat.info_save import StoredUrl
from env import Environment
from repository.types import ConversationModel, UserModel

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

AnswerPart = TextAnswer | StoredUrl

class Answer(BaseModel):
    content: AnswerPart
    quotes: list[Quote] = []

@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Dependencies:
    env: Environment
    google_client: AsyncClient
    bq_client: bigquery.Client
    quotes: list[Quote]
    conversation: ConversationModel
    user: UserModel


MessageContent = ModelMessage

MessagesContentTypeAdapter = TypeAdapter(
    list[MessageContent],
    config=ConfigDict(defer_build=True, ser_json_bytes="base64", val_json_bytes="base64"),
)
