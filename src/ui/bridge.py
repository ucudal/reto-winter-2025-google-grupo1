from collections.abc import AsyncIterable
import mimetypes
from pathlib import Path

from gradio import Component
from pydantic_ai import BinaryContent
from pydantic_ai.messages import UserPromptPart
from chat.factory import BotFactory
from chat.info_save import StoredUrl, upload
from env import env
from ui.types import Renderable, UserInput, OutputDir
from ui.details import render_quotes
from ui.file_renderer import render_binary


def read_file(file_path: Path) -> BinaryContent | None:
    path = Path(file_path)

    file_data = path.read_bytes()

    mimetype, _ = mimetypes.guess_type(path)

    if mimetype is None:
        return None

    return BinaryContent(data=file_data, media_type=mimetype)


async def handle_file(file: BinaryContent) -> StoredUrl:
    return await upload(file, credentials=env().credentials)

def get_bot():
    return BotFactory().default()


async def ui_to_chat(message: UserInput) -> AsyncIterable[Renderable]:
    files = (read_file(Path(file)) for file in message["files"])
    files = [await handle_file(file) for file in files if file]

    user_prompt = UserPromptPart(files + [message["text"]])

    response = get_bot().answer(user_prompt)

    chunk = None
    content = None

    async for chunk in response:
        content = chunk.content
        match content.kind:
            case "text":
                content = content.text
            case _:
                content = assistant(render_binary(content))

        yield content

    if content is None or chunk is None:
        yield "No content"
        return

    yield [
        assistant(render_quotes(chunk.quotes)),
        content,
    ]

def assistant(val: str | Component) -> OutputDir:
    return { "role": "assistant", "content": val}
