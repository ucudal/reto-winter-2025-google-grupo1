# Rabbit, you son of a lovely lady, this file is for goofing around and testing
# stuff. Please, for all that is holy, do not bother me in prs with this file
# or duplicated functionality because of the mess that this file is.
import json
from pydantic_ai.messages import ModelMessagesTypeAdapter
from chat.memory import MEMORY_DIR
from datetime import datetime

from prompts.base_prompt import get_base_prompt
from prompts.system_prompt import SystemPromptParams, get_system_prompt

def main() -> None:
    path = MEMORY_DIR / "schema.json"
    _ = path.write_text(json.dumps(ModelMessagesTypeAdapter.json_schema()))

    system_prompt = get_system_prompt(
        params=SystemPromptParams(date=datetime.now())
    )
    print(system_prompt)


if __name__ == "__main__":
    main()
