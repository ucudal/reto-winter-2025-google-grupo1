from typing import assert_never
import gradio as gr

from pydantic_ai import AudioUrl, DocumentUrl, ImageUrl, VideoUrl

from chat.info_save import StoredUrl

def render_binary(content: StoredUrl) -> gr.Component:
    match content:
        case ImageUrl():
            return gr.Video(value=content.media_type)
        case AudioUrl():
            return gr.Audio(value=content.media_type)
        case DocumentUrl():
            return gr.File(value=content.media_type)
        case VideoUrl():
            return gr.Audio(value=content.media_type)

    assert_never(content)
