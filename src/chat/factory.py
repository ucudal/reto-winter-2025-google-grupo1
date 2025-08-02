from typing import Callable
from chat.chat import Bot
from chat.tools.example import example_tool_func
from env import env

tools=list[Callable[..., object]]()

if env().environment == "dev":
    tools.append(example_tool_func)

class BotFactory:
    def default(self):
        return Bot(tool_bag=tools, api_key=env().google_cloud_api_key)
