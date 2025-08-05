from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from jinja2 import Template
from functools import cache
from pydantic import BaseModel, Field

TEMPLATES_FOLDER = Path(__file__).parent / "templates"

@cache
def _load_base_prompt(file_path: Path) -> str:
    """
    Load a prompt from a file, and cache it.

    Args:
        file_path (str): The path to the base prompt file.

    Returns:
        str: The content of the base prompt file.
    """
    return file_path.read_text()

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

def render_prompt(path: Path, params: Mapping[str, object]):
    return _generate_base_prompt(_load_base_prompt(path), params)
