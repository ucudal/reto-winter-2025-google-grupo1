from collections.abc import AsyncIterable
from functools import cache
import mimetypes
from pathlib import Path

from pydantic_ai import BinaryContent
from pydantic_ai.messages import TextPart, UserPromptPart
from chat.factory import BotFactory
from chat.info_save import upload
from env import env
from ui.types import UserInput


def read_file(file_path: Path) -> BinaryContent | None:
    path = Path(file_path)

    file_data = path.read_bytes()

    mimetype, _ = mimetypes.guess_type(path)

    if mimetype is None:
        return None

    return BinaryContent(
        data=file_data,
        media_type=mimetype
    )

async def handle_file(file: BinaryContent):
    return await upload(file)

@cache
def get_bot():
    return BotFactory().default()

async def ui_to_chat(message: UserInput) -> AsyncIterable[UserInput]:
    files = (read_file(Path(file)) for file in message["files"])
    files = [await handle_file(file) for file in files if file]

    text = TextPart(content=message["text"])
    user_prompt = UserPromptPart(files + [message["text"]])

    response = get_bot().answer(user_prompt, user_id=env().user_id)

    text = ""

    async for chunk in response:
        text = chunk
        yield {"text": text, "files": []}


    yield {"text": text or "What", "files": []}

