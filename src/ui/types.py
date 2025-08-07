from typing import Literal, TypedDict

import gradio


class UserInput(TypedDict):
    text: str
    files: list[str]

class OutputDir(TypedDict):
    role: Literal["user", "assistant"]
    content: str | gradio.Component


type Renderable = str | OutputDir | list["Renderable"]

# Define a type alias for a single message in the history, which can be text
# or a file tuple. A file is represented as a tuple, e.g., ('/path/to/file.png',).
Message = str | tuple[str] | None

# History is a list of user/assistant message pairs.
ChatHistory = list[tuple[Message, Message]]
