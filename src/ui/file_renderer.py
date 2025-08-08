from typing import assert_never
import gradio as gr

from pydantic_ai import AudioUrl, BinaryContent, DocumentUrl, ImageUrl, VideoUrl

from chat.info_save import StoredUrl

def render_binary(content: StoredUrl) -> gr.Component:
    print(f"{content = }")

    return content.url # pyright: ignore[reportReturnType]

    assert_never(content)
