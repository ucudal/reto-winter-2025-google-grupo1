from typing import final

from pydantic_ai import Agent
from pydantic_ai.messages import UserPromptPart
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider

from chat.memory import retrieve_conversation, set_conversation
from chat.tools import toolset
from chat.types import Dependencies, UserId
from env import Environment


@final
class Bot:
    def __init__(
        self, *, env: Environment, chats: dict[UserId, Agent[Dependencies, str]] | None = None
    ) -> None:
        self.chats = chats or {}
        self.__env = env

    def make_agent(self) -> Agent[Dependencies, str]:
        return Agent(
            GoogleModel(
                "gemini-2.5-pro",
                provider=GoogleProvider(api_key=self.__env.google_cloud_api_key),
                settings=GoogleModelSettings(),
            ),
            toolsets=[toolset.main_toolset],
            deps_type=Dependencies,
        )

    def get_agent(self, userId: UserId) -> Agent[Dependencies, str]:
        agent = self.chats.get(userId)

        if agent is None:
            agent = self.make_agent()
            self.chats[userId] = agent

        return agent

    def get_dependencies(self) -> Dependencies:
        return Dependencies(env=self.__env)

    async def answer(self, message: UserPromptPart, /, *, user_id: UserId):
        agent = self.get_agent(user_id)
        history = retrieve_conversation(user_id)

        async with agent.run_stream(
            user_prompt=message.content, deps=self.get_dependencies(), message_history=history
        ) as response:
            async for chunk in response.stream():
                yield chunk

            history = response.all_messages()

        set_conversation(user_id, history)
