from collections.abc import AsyncIterable
import mimetypes
from pathlib import Path
from typing import assert_never

from gradio import Component
from pydantic_ai import BinaryContent
from pydantic_ai.messages import UserPromptPart
from chat.factory import BotFactory
from ui.details import render_quotes
from ui.types import OutputDir, Renderable, UserInput
from ui.file_renderer import render_binary


def handle_file(file_path: Path) -> BinaryContent | None:
    path = Path(file_path)

    file_data = path.read_bytes()

    mimetype, _ = mimetypes.guess_type(path)

    if mimetype is None:
        return None

    return BinaryContent(data=file_data, media_type=mimetype)


def get_bot():
    return BotFactory().default()


async def ui_to_chat(message: UserInput) -> AsyncIterable[Renderable]:
    files = [handle_file(Path(file)) for file in message["files"]]
    files = [file for file in files if file]

    user_prompt = UserPromptPart(files + [message["text"]])

    response = get_bot().answer(user_prompt)

    chunk = None
    content = None

    async for chunk in response:
        content = chunk.content
        match content.kind:
            case "text":
                content = content.text
            case "binary":
                # Untested, also, horribly, terribly inefficient. Shameful.
                # Disgraceful.
                content = assistant(render_binary(content))
            case _:
                assert_never(content.kind)

        yield content

    if content is None or chunk is None:
        yield "No content"
        return

    yield [
        {"role": "assistant", "content": render_quotes(chunk.quotes)},
        content,
    ]

def assistant(val: str | Component) -> OutputDir:
    return { "role": "assistant", "content": val}
