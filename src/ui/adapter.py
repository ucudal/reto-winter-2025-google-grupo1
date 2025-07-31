from collections.abc import Sequence
import mimetypes
from pathlib import Path

from google.genai.types import Part
from chat.chat import answer
from ui.types import UserInput

def handle_files(files: Sequence[Path]) -> list[Part]:
    """
    Convert a sequence of local file paths into a list of Part objects with appropriate MIME types for API use.
    
    Each file is read as bytes, its MIME type is determined (defaulting to "application/octet-stream" if unknown), and a Part object is created for each file.
    
    Parameters:
        files (Sequence[Path]): Local file paths to be converted.
    
    Returns:
        list[Part]: List of Part objects representing the files.
    """
    parts = list[Part]()
    for path in files:
        mime_type, _ = mimetypes.guess_type(path)

        if mime_type is None:
            mime_type = "application/octet-stream"

        file_bytes = Path(path).read_bytes()

        # Create the Part object with the file's data and MIME type
        parts.append(Part.from_bytes(data=file_bytes, mime_type=mime_type))

    return parts

def ui_to_chat(message: UserInput) -> UserInput:
    """
    Converts a user input message into a chat-compatible format and retrieves the chat response.
    
    Parameters:
        message (UserInput): A dictionary containing user text and a list of file paths.
    
    Returns:
        UserInput: A dictionary with the chat response text and an empty list of files.
    """
    files = handle_files([Path(file) for file in message["files"]])
    text = Part.from_text(text=message["text"])

    response = answer(files + [text])


    return { "text": response[0].text or "What", "files": [] }
