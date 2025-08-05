from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field
from prompts.base_prompt import TEMPLATES_FOLDER, render_prompt

system_prompt_path = TEMPLATES_FOLDER / "system_prompt_template.md"

class SystemPromptParams(BaseModel):
    date: datetime = Field(default_factory=datetime.now)


def render_system_prompt(prompt_params: SystemPromptParams, *, path: Path = system_prompt_path) -> str:
    return render_prompt(path, prompt_params.model_dump(mode="json"))
