from twitchio.ext import commands

from bot.config import ACCESS_TOKEN, CHANNELS, PREFIX
from logs import logger


class YeppBot(commands.Bot):
    def __init__(self):
        super().__init__(token=ACCESS_TOKEN, prefix=PREFIX, initial_channels=CHANNELS)

    async def event_ready(self):
        logger.info(f'Logged in as | {self.nick}')

    async def event_command_error(self, ctx, exc):
        logger.error(exc, exc_info=True)


yepp_bot = YeppBot()
yepp_bot.load_module("bot.cogs")
