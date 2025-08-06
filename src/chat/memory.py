from pathlib import Path

from pydantic import ConfigDict, TypeAdapter
from pydantic_ai.messages import ModelMessage

MEMORY_DIR = Path(__file__).parent / "../../memory/"

# Currently this is so stupidly inefficient. I'll wait to have the db to fix
# it, tho.

MessageContent = ModelMessage

MessagesContentTypeAdapter = TypeAdapter(
    list[MessageContent],
    config=ConfigDict(defer_build=True, ser_json_bytes="base64", val_json_bytes="base64"),
)


def set_conversation(user_id: str, history: list[ModelMessage]):
    path = get_path(user_id)

    _ = path.write_bytes(MessagesContentTypeAdapter.dump_json(history))


def retrieve_conversation(user_id: str) -> list[ModelMessage]:
    path = get_path(user_id)

    if not path.exists():
        return []

    return MessagesContentTypeAdapter.validate_json(path.read_bytes())


def get_path(user_id: str):
    return MEMORY_DIR / f"{user_id}.json"
