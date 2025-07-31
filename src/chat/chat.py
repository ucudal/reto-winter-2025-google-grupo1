from collections.abc import Iterator, Sequence
from collections.abc import Sequence
from functools import cache
from google import genai
from google.genai.types import Part
from env import env


@cache
def get_client(api_key: str):
    return genai.Client(api_key=api_key)


@cache
def get_chat(id: str):
    return get_client(env().google_cloud_api_key).chats.create(model="gemini-2.0-flash")


def answer(message: Sequence[Part]) -> Iterator[list[Part]]:
    chat = get_chat("test")

    response = chat.send_message_stream(list(message))

    for chunk in response:
        if (
            not chunk.candidates
            or not chunk.candidates[0].content
            or not chunk.candidates[0].content.parts
        ):
            yield [Part.from_text(text="Ocurrió un error")]
            return

        yield chunk.candidates[0].content.parts

def get_history() -> list[Part]: ...
