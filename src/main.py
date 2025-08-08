# Rabbit, you son of a lovely lady, this file is for goofing around and testing
# stuff. Please, for all that is holy, do not bother me in prs with this file
# or duplicated functionality because of the mess that this file is.
from datetime import datetime

from chat.factory import BotFactory
from env import env
from prompts.system_prompt import SystemPromptParams, get_system_prompt

import asyncio
from rag.rag import RAGTool
from rag.types import RAGQuery


async def main() -> None:
    tool = RAGTool(deps=BotFactory().get_default_dependencies(env()))

    result = await tool.retrieve_with_vector_search(
        RAGQuery(query="Qué cursos electivos puedo hacer en ithaka?")
    )

    print(f"{result = }")

    system_prompt = get_system_prompt(params=SystemPromptParams(date=datetime.now()))
    print(system_prompt)


if __name__ == "__main__":
    asyncio.run(main())
