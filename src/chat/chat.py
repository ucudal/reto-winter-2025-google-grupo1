from collections.abc import Sequence
from functools import cache
from typing import Callable, final
from google import genai
from google.genai.chats import Chat
from google.genai.types import (
    GenerateContentConfig,
    Part,
)

UserId = str


@cache
def get_client(api_key: str):
    return genai.Client(api_key=api_key)


@final
class Bot:
    def __init__(
        self, *, tool_bag: list[Callable[..., object]], api_key: str, chats: dict[UserId, Chat] | None = None
    ) -> None:
        self.chats = chats or {}
        self.__api_key = api_key
        self.tool_bag = tool_bag

    def get_tools(self):
        print(f"{self.tool_bag = }")
        return self.tool_bag

    def make_chat(self) -> Chat:
        return get_client(self.__api_key).chats.create(model="gemini-2.0-flash")

    def get_chat(self, userId: UserId) -> Chat:
        chat = self.chats.get(userId)

        if chat is None:
            chat = self.make_chat()
            self.chats[userId] = chat

        return chat

    def answer(self, message: Sequence[Part], /, *, user_id: UserId) -> list[Part]:
        chat = self.get_chat(user_id)

        response = chat.send_message(
            list(message),
            config=GenerateContentConfig(tools=self.get_tools()),
        )

        if (
            not response.candidates
            or not response.candidates[0].content
            or not response.candidates[0].content.parts
        ):
            print(f"{response = }")
            return [Part.from_text(text="Ocurrió un error")]

        return response.candidates[0].content.parts
