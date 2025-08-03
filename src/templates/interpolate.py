from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel


class PromptManager(BaseModel):
    template_dir: str = "prompts/system"

    def __post_init__(self):
        self.env: Environment = Environment(loader=FileSystemLoader(self.template_dir))

    def render_prompt(self, template_name: str, vars: dict[str, object]) -> str:
        template = self.env.get_template(f"{template_name}.md")
        return template.render(**vars)
