from pydantic import BaseModel, Field

from datetime import datetime

from prompts.base_prompt import get_base_prompt


class SystemPromptParams(BaseModel):
    date: datetime = Field(default_factory=datetime.now)

def get_system_prompt(params: SystemPromptParams) -> str:
    """
    Get a system prompt for the chatbot.

    Args:
        params (SystemPromptParams): Parameters to render in the template.

    Returns:
        str: The system prompt.
    """
    return get_base_prompt(file_path=r"src/prompts/templates/system_prompt_template.md", prompt_params=params.model_dump(mode="json"))
