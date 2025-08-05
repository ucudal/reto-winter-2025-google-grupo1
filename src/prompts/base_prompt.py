from datetime import datetime
from typing import Mapping
from jinja2 import Template
from functools import cache
from pydantic import BaseModel, Field

@cache
def _load_base_prompt(file_path: str) -> str:
    """
    Load a prompt from a file.

    Args:
        file_path (str): The path to the base prompt file.

    Returns:
        str: The content of the base prompt file.
    """
    with open(file_path, 'r') as file:
        return file.read()

def _generate_base_prompt(template_str: str, prompt_params: Mapping[str, object]) -> str:
    """
    Generate a prompt using a template string and parameters.

    Args:
        template_str (str): The template string to use for generating the prompt.
        params (dict[str, object]): Parameters to render in the template.

    Returns:
        str: The generated base prompt.
    """
    template = Template(template_str)
    return template.render(**prompt_params)

class BasePromptParams(BaseModel):
    date: datetime = Field(default_factory=datetime.now)

def get_base_prompt(file_path: str, prompt_params: BasePromptParams) -> str:
    """
    Get a prompt for the chatbot.

    Args:
        file_path (str): The path to the base prompt file.
        params (dict[str, object]): Parameters to render in the template.

    Returns:
        str: The base prompt.
    """
    return _generate_base_prompt(_load_base_prompt(file_path), prompt_params.model_dump(mode="json"))
