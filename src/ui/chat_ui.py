from collections.abc import Iterator
import gradio

from ui.adapter import ui_to_chat
from ui.types import UserInput


def resolve(message: UserInput, _history: list[gradio.MessageDict]) -> Iterator[str]:
    chunk = None

    # TODO: Implement file handling for return types.
    for chunk in ui_to_chat(message):
        yield chunk["text"]

    return chunk

def main():
    """
    Sets up and launches the Gradio Chat Interface.
    """
    demo = gradio.ChatInterface(
        fn=resolve,
        multimodal=True,
        type="messages",
        textbox=gradio.MultimodalTextbox(
            sources=["microphone", "upload"],
        ),
        title="🖼️ Multimodal Chat Assistant",
        description="Feel free to send a message, an image, or both!",
        flagging_mode="manual",
        flagging_options=["Like", "Spam", "Inappropriate", "Other"],
    )

    _ = demo.launch(pwa=True)


if __name__ == "__main__":
    main()
