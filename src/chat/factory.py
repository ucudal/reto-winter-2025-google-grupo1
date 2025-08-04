from chat.bot import Bot
from chat.tools.toolset import main_toolset
from env import env

class BotFactory:
    def default(self):
        return Bot(env=env(), toolset=main_toolset)
