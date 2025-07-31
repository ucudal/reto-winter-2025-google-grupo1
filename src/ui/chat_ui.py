from pathlib import Path
from typing import TypedDict
import gradio

from ui.adapter import ui_to_chat
from ui.types import UserInput

def resolve(message: UserInput, _history: list[str]):
    """
    Converts a user input message to a chat-compatible format and yields the result.
    
    Parameters:
        message (UserInput): The user input to be processed.
    
    Yields:
        The chat-formatted representation of the user input.
    """
    yield ui_to_chat(message)

def main():
    """
    Initialize and launch the multimodal Gradio chat interface for user interaction.
    
    The interface supports text and image inputs, provides manual flagging options, and displays a custom title and description.
    """
    demo = gradio.ChatInterface(
        fn=resolve,
        multimodal=True,
        title="🖼️ Multimodal Chat Assistant",
        description="Feel free to send a message, an image, or both!",
        flagging_mode="manual",
        flagging_options=["Like", "Spam", "Inappropriate", "Other"],
    )

    _ = demo.launch()



if __name__ == "__main__":
    main()
