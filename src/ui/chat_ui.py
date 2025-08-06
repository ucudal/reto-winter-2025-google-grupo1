from collections.abc import AsyncGenerator
import gradio

from ui.bridge import ui_to_chat
from ui.types import Renderable, UserInput


async def resolve(message: UserInput, _history: list[str]) -> AsyncGenerator[Renderable]:
    async for chunk in ui_to_chat(message):
        yield chunk


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
        textbox=gradio.MultimodalTextbox(sources=["microphone", "upload"]),
    )

    _ = demo.launch()


if __name__ == "__main__":
    main()
