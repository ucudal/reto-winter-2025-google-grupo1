from collections.abc import AsyncGenerator, Sequence
from typing import assert_never, final

from google.genai.types import HarmBlockThreshold, HarmCategory
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelRequest, UserPromptPart
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.toolsets import AbstractToolset

from chat.info_save import upload
from chat.memory import add_message
from chat.types import Answer, Dependencies, TextAnswer
from prompts.system_prompt import SystemPromptParams, get_system_prompt
from textToSpeech.textToSpeech import TextToSpeechService


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
            system_prompt=get_system_prompt(SystemPromptParams()),
        )

    def get_dependencies(self) -> Dependencies:
        return self._deps

    def get_history(self) -> list[ModelMessage]:
        output = list[ModelMessage]()

        for message in self.get_dependencies().conversation.messages:
            output.extend(message.message_text)

        return output

    def _storeInput(self, message: UserPromptPart):
        print("\n\nStart message.")
        print("Saving user message.")
        add_message(self.get_dependencies(), "user", [ModelRequest(parts=[message])])

    def include_extra_data(self, answer: Answer) -> Answer:
        answer.quotes += self.get_dependencies().quotes
        return answer

    async def answer_with_audio(self, message: UserPromptPart, /) -> Answer:
        agent = self.make_agent()
        dependencies = self.get_dependencies()

        output = await agent.run(
            user_prompt=message.content, deps=dependencies, message_history=self.get_history()
        )
        result = await upload(
            await TextToSpeechService().generate_audio(
                output.output
            )
        )

        return self.include_extra_data(Answer(content=result))

    async def answer_with_text(self, message: UserPromptPart, /) -> AsyncGenerator[Answer]:
        agent = self.make_agent()
        dependencies = self.get_dependencies()

        self._storeInput(message)

        chunk = TextAnswer(text="")

        async with agent.run_stream(
            user_prompt=message.content, deps=dependencies, message_history=self.get_history()
        ) as response:
            async for chunk in response.stream():
                chunk = TextAnswer(text=chunk)
                yield Answer(content=chunk)

            new_messages = response.new_messages()

        yield self.include_extra_data(Answer(content=chunk, quotes=dependencies.quotes))
        await self._finish(new_messages)

    async def answer(self, message: UserPromptPart, /) -> AsyncGenerator[Answer]:
        kind = self.get_dependencies().env.answer

        match kind:
            case "text":
                async for chunk in self.answer_with_text(message):
                    yield chunk
                return
            case "audio":
                yield await self.answer_with_audio(message)
                return

        assert_never(kind)

    async def _finish(self, message: Sequence[ModelMessage]):
        print("End message.")
        add_message(self.get_dependencies(), "assistant", message)
        print("Saved message.")
