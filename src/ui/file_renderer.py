import base64
import gradio as gr

from pydantic_ai import BinaryContent

def to_data_uri(data: bytes, media_type: str) -> str:
    """Encodes binary data into a Base64 data URI."""
    base64_data = base64.b64encode(data).decode('utf-8')
    return f"data:{media_type};base64,{base64_data}"

def render_video(content: BinaryContent) -> gr.Video:
    data_uri = to_data_uri(content.data, content.media_type)
    return gr.Video(value=data_uri)

def render_audio(content: BinaryContent) -> gr.Audio:
    data_uri = to_data_uri(content.data, content.media_type)
    return gr.Audio(value=data_uri)

def render_image(content: BinaryContent) -> gr.Image:
    data_uri = to_data_uri(content.data, content.media_type)
    return gr.Image(value=data_uri, show_label=False)

def render_file(content: BinaryContent) -> gr.File:
    data_uri = to_data_uri(content.data, content.media_type)

    return gr.File(value=data_uri)

def render_binary(content: BinaryContent) -> gr.Component:
    if content.is_video:
        return render_video(content)
    if content.is_audio:
        return render_audio(content)
    if content.is_image:
        return render_image(content)

    return render_file(content)
