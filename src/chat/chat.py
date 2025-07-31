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


def answer(message: Sequence[Part]) -> list[Part]:
    chat = get_chat("test")

    response = chat.send_message(list(message))

    if (
        not response.candidates
        or not response.candidates[0].content
        or not response.candidates[0].content.parts
    ):
        return [Part.from_text(text="Ocurrió un error")]

    return response.candidates[0].content.parts


def get_history() -> list[Part]: ...
