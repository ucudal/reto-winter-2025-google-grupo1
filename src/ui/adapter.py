from collections.abc import Iterator, Sequence
import mimetypes
from pathlib import Path

from google.genai.types import Part
from chat.chat import answer
from ui.types import UserInput


def handle_files(files: Sequence[Path]) -> list[Part]:
    """
    Converts a list of local file paths into a list of API-ready Part objects.

    This function reads each file as bytes and packages it with its
    MIME type into a Part object for the Gemini API.
    """
    parts = list[Part]()
    for path in files:
        mime_type, _ = mimetypes.guess_type(path)

        if mime_type is None:
            mime_type = "application/octet-stream"

        # Create the Part object with the file's data and MIME type
        parts.append(Part.from_bytes(data=path.read_bytes(), mime_type=mime_type))

    return parts


def ui_to_chat(message: UserInput) -> Iterator[UserInput]:
    files = handle_files([Path(file) for file in message["files"]])
    text = Part.from_text(text=message["text"])

    response = answer(files + [text])

    text = ""

    for chunk in response:
        text += chunk[0].text or ""
        yield {"text": text or "What", "files": []}

