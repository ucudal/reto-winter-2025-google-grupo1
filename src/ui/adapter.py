from collections.abc import Iterable, Iterator
import mimetypes
from pathlib import Path
from typing import cast

from google.genai.types import Part
from gradio import Component
from chat.chat import answer
from ui.types import Content, UserInput

MimeType = str

def handle_files(files: Iterable[tuple[Path, MimeType | None]]) -> list[Part]:
    """
    Converts a list of local file paths into a list of API-ready Part objects.

    This function reads each file as bytes and packages it with its
    MIME type into a Part object for the Gemini API.
    """
    parts = list[Part]()

    for path, mime_type in files:

        if mime_type is None:
            mime_type, _ = mimetypes.guess_type(path)

        assert mime_type is not None

        parts.append(Part.from_bytes(data=path.read_bytes(), mime_type=mime_type))

    return parts

def extract_parts(content: UserInput) -> list[Part]:
    paths = ((Path(path), None) for path in content["files"])
    return [Part.from_text(text=content["text"])] + list(handle_files(paths))

def ui_to_chat(message: UserInput) -> Iterator[UserInput]:
    parts = extract_parts(message)

    response = answer(parts)

    text = ""

    for chunk in response:
        text += chunk[0].text or ""
        yield {"text": text or "What", "files": []}
