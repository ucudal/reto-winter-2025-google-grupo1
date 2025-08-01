from typing import TypedDict

from gradio import Component
from gradio.components.chatbot import FileDataDict

Content = str | FileDataDict | tuple[object, ...] | Component


class UserInput(TypedDict):
    text: str
    files: list[str]


# Define a type alias for a single message in the history, which can be text
# or a file tuple. A file is represented as a tuple, e.g., ('/path/to/file.png',).
Message = str | tuple[str] | None

# History is a list of user/assistant message pairs.
ChatHistory = list[tuple[Message, Message]]
