from collections.abc import AsyncGenerator
from typing import final

from google.genai.types import HarmBlockThreshold, HarmCategory
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelRequest, UserPromptPart
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.toolsets import AbstractToolset

from chat.memory import add_message
from chat.types import Answer, Dependencies, TextAnswer
from prompts.system_prompt import SystemPromptParams, get_system_prompt


@final
class Bot:
    def __init__(
        self,
        *,
        deps: Dependencies,
        toolset: AbstractToolset[Dependencies],
    ) -> None:
        self._deps = deps
        self.__toolset = toolset

    def make_agent(self) -> Agent[Dependencies, str]:
        return Agent(
            GoogleModel(
                "gemini-2.5-pro",
                provider=GoogleProvider(api_key=self.get_dependencies().env.google_cloud_api_key),
                settings=GoogleModelSettings(
                    temperature=0.2,
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
            system_prompt=get_system_prompt(SystemPromptParams())
        )

    def get_dependencies(self) -> Dependencies:
        return self._deps

    def get_history(self) -> list[ModelMessage]:
        output = list[ModelMessage]()

        for message in self.get_dependencies().conversation.messages:
            output.extend(message.message_text)

        return output

    async def answer(self, message: UserPromptPart, /) -> AsyncGenerator[Answer]:
        deps = self.get_dependencies()
        agent = self.make_agent()
        dependencies = self.get_dependencies()

        print("\n\nStart message.")
        print("Saving user message.")

        add_message(deps, "user", [ModelRequest(parts=[message])])

        chunk = TextAnswer(text="")

        async with agent.run_stream(
            user_prompt=message.content, deps=dependencies, message_history=self.get_history()
        ) as response:
            async for chunk in response.stream():
                chunk = TextAnswer(text=chunk)
                yield Answer(content=chunk)

            new_messages = response.new_messages()

        yield Answer(content=chunk, quotes=dependencies.quotes)
        print("End message.")

        add_message(deps, "assistant", new_messages)

        print("Saved message.")
