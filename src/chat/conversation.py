from pydantic_ai import Agent
from pydantic_ai.models import Model
from pydantic_ai.toolsets import AbstractToolset

from chat.dependencies import Dependencies

async def start_conversation(model: Model, toolset: AbstractToolset) -> Agent[Dependencies]:

    return output
