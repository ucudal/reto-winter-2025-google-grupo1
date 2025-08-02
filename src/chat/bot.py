from typing import final

from pydantic_ai import Agent
from pydantic_ai.messages import UserPromptPart
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.settings import ModelSettings
from pydantic_ai.providers.google import GoogleProvider

from chat.dependencies import Dependencies
from chat.tools import toolset
from env import Environment

UserId = str

@final
class Bot:
    def __init__(
        self, *, env: Environment, chats: dict[UserId, Agent[Dependencies, str]] | None = None
    ) -> None:
        self.chats = chats or {}
        self.__env = env

    def make_agent(self) -> Agent[Dependencies, str]:
        return Agent(
            GoogleModel("gemini-2.5-flash", provider=GoogleProvider(api_key=self.__env.google_cloud_api_key), settings=ModelSettings()),
            toolsets=[toolset.main_toolset],
            deps_type=Dependencies

        )

    def get_agent(self, userId: UserId) -> Agent[Dependencies, str]:
        agent = self.chats.get(userId)

        if agent is None:
            agent = self.make_agent()
            self.chats[userId] = agent

        return agent

    def get_dependencies(self) -> Dependencies:
        return Dependencies(
            env=self.__env
        )

    async def answer(self, message: UserPromptPart, /, *, user_id: UserId):
        agent = self.get_agent(user_id)

        async with agent.run_stream(user_prompt=message.content, deps=self.get_dependencies()) as response:
            async for chunk in response.stream():
                yield chunk
