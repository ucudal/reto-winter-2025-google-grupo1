from collections.abc import Iterator
import gradio

from ui.adapter import ui_to_chat
from ui.types import UserInput


def resolve(message: UserInput, _history: list[str]) -> Iterator[str]:
    for chunk in ui_to_chat(message):
        yield chunk["text"]


def main():
    """
    Sets up and launches the Gradio Chat Interface.
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
