from typing import final

from google.genai.types import HarmBlockThreshold, HarmCategory
from pydantic_ai import Agent
from pydantic_ai.messages import UserPromptPart
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.toolsets import AbstractToolset

from chat.clients import create_google_client
from chat.memory import retrieve_conversation, set_conversation
from chat.types import Dependencies, UserId
from env import Environment


@final
class Bot:
    def __init__(
        self,
        *,
        env: Environment,
        toolset: AbstractToolset[Dependencies],
        chats: dict[UserId, Agent[Dependencies, str]] | None = None,
    ) -> None:
        self.chats = chats or {}
        self.__env = env
        self.__toolset = toolset

    def make_agent(self) -> Agent[Dependencies, str]:
        return Agent(
            GoogleModel(
                "gemini-2.5-pro",
                provider=GoogleProvider(api_key=self.__env.google_cloud_api_key),
                settings=GoogleModelSettings(
                    temperature=0.6,
                    google_safety_settings=[
                        {
                            "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                        }
                    ],
                ),
            ),
            toolsets=[self.__toolset],
            output_retries=10,
            deps_type=Dependencies,
        )

    def get_agent(self, userId: UserId) -> Agent[Dependencies, str]:
        agent = self.chats.get(userId)

        if agent is None:
            agent = self.make_agent()
            self.chats[userId] = agent

        return agent

    def get_dependencies(self) -> Dependencies:
        return Dependencies(
            env=self.__env,
            bq_client=create_bq_client(self.__env.project_id),
            google_client=create_google_client(self.__env.google_cloud_api_key).aio,
        )

    async def answer(self, message: UserPromptPart, /, *, user_id: UserId):
        agent = self.get_agent(user_id)
        history = retrieve_conversation(user_id)

        print("\n\nStart message.")

        async with agent.run_stream(
            user_prompt=message.content, deps=self.get_dependencies(), message_history=history
        ) as response:
            async for chunk in response.stream():
                yield chunk

            history = response.all_messages()

        print("End message.")

        set_conversation(user_id, history)
