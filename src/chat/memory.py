from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import assert_never
from uuid import uuid4

from pydantic_ai.messages import ModelMessage

from chat.types import Dependencies
from repository.conversation import ConversationRepository
from repository.message import MessageRepository
from repository.types import ConversationModel, MessageModel, SenderType

MEMORY_DIR = Path(__file__).parent / "../../memory/"

def add_message(
    deps: Dependencies,
    sender: SenderType,
    message: Sequence[ModelMessage],
) -> None:
    memory = deps.env.memory
    user_id = deps.user.user_id
    conversation_id = deps.conversation.conversation_id

    match memory:
        case "bigquery":
            _ = MessageRepository(deps.bq_client, deps.env.project_id, deps.env.dataset).create(conversation_id, sender, message)
            return
        case "local":
            conversation = retrieve_conversation(deps)

            assert conversation is not None

            conversation.messages.append(MessageModel(
                message_id=str(uuid4()),
                conversation_id=conversation_id,
                message_text=list(message),
                sender=sender,
                timestamp=datetime.now(timezone.utc)
            ))

            _ = get_path(user_id, conversation_id).write_text(conversation.model_dump_json())
            return

    assert_never(memory)



def retrieve_conversation(
    deps: Dependencies
) -> ConversationModel | None:
    memory = deps.env.memory
    user_id = deps.user.user_id
    conversation_id = deps.conversation.conversation_id

    match memory:
        case "bigquery":
            return ConversationRepository(
                deps.bq_client, deps.env.project_id, deps.env.dataset
            ).read(conversation_id)
        case "local":
            path = get_path(user_id, conversation_id)

            if not path.exists():
                return None

            return ConversationModel.model_validate_json(path.read_text())

    assert_never(memory)


def get_path(user_id: str, conversation_id: str):
    return MEMORY_DIR / f"conversation_{conversation_id}_of_user_{user_id}.json"
