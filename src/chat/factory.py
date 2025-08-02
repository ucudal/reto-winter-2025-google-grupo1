from chat.bot import Bot
from env import env

class BotFactory:
    def default(self):
        return Bot(env=env())
