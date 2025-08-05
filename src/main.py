# Rabbit, you son of a lovely lady, this file is for goofing around and testing
# stuff. Please, for all that is holy, do not bother me in prs with this file
# or duplicated functionality because of the mess that this file is.
import json
from pydantic_ai.messages import ModelMessagesTypeAdapter
from chat.memory import MEMORY_DIR
from datetime import datetime

from prompts.base_prompt import get_base_prompt
from prompts.system_prompt import SystemPromptParams, get_system_prompt

import asyncio
from google import genai
from google.cloud import bigquery
from chat.types import Dependencies
from env import env
from rag.rag import RAGTool
from rag.types import RAGQuery


async def main() -> None:
    tool = RAGTool(
        deps=Dependencies(
            env=env(),
            bq_client=bigquery.Client(project=env().project_id),
            google_client=genai.Client(api_key=env().google_cloud_api_key).aio,
        )
    )

    result = await tool.retrieve_with_vector_search(
        RAGQuery(query="Qué cursos electivos puedo hacer en ithaka?")
    )

    print(f"{result = }")

    system_prompt = get_system_prompt(
        params=SystemPromptParams(date=datetime.now())
    )
    print(system_prompt)


if __name__ == "__main__":
    asyncio.run(main())
