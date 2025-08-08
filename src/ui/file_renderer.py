from typing import assert_never
import gradio as gr

from pydantic_ai import AudioUrl, DocumentUrl, ImageUrl, VideoUrl

from chat.info_save import StoredUrl

def render_binary(content: StoredUrl) -> gr.Component:
    match content:
        case ImageUrl():
            return gr.Image(value=content.url)
        case AudioUrl():
            return gr.Audio(value=content.url)
        case DocumentUrl():
            return gr.File(value=content.url)
        case VideoUrl():
            return gr.Video(value=content.url)

    assert_never(content)
