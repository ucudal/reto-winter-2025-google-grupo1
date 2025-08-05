from typing import final

from google.genai.types import HarmBlockThreshold, HarmCategory
from pydantic_ai import Agent
from pydantic_ai.messages import UserPromptPart
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.toolsets import AbstractToolset

from chat.memory import retrieve_conversation, set_conversation
from chat.types import Dependencies, UserId
from env import Environment
from prompts.system_prompt import SystemPromptParams, render_system_prompt


@final
class Bot:
    def __init__(
        self,
        *,
        env: Environment,
        toolset: AbstractToolset[Dependencies],
    ) -> None:
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
            system_prompt=self.get_system_prompt(),
            deps_type=Dependencies,
        )

    def get_system_prompt(self):
        return render_system_prompt(SystemPromptParams())

    def get_dependencies(self) -> Dependencies:
        return Dependencies(env=self.__env)

    async def answer(self, message: UserPromptPart, /, *, user_id: UserId):
        agent = self.make_agent()
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
