from datetime import datetime, timezone
from typing import ClassVar, Literal
import uuid

from pydantic import BaseModel, ConfigDict, Field
from pydantic_ai.messages import ModelMessage


class UserModel(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


SenderType = Literal["user", "assistant"]


class MessageModel(BaseModel):
    message_id: str
    conversation_id: str
    sender: SenderType
    # A singular message may contain multiple parts (text, quotes, files)
    message_text: list[ModelMessage]
    # I wonder how precise this is, since I will be creating both the user
    # prompt and and model question at the same time.
    timestamp: datetime | None

    model_config: ClassVar[ConfigDict] = ConfigDict(
        ser_json_bytes="base64",
        val_json_bytes="base64"
    )


class ConversationCreationModel(BaseModel):
    conversation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ConversationModel(ConversationCreationModel):
    messages: list[MessageModel] = []
