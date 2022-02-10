import re

from twitchio.ext import commands

from logs import logger


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(self, ctx: commands.Context, exc: Exception):
        logger.error(exc, exc_info=True)

    @staticmethod
    def get_mentioned_user(*args: str):
        if args:
            if match := re.search(r'\s*@?(?P<username>[a-zA-Z0-9_]{4,25}),?\s*', args[0]):
                return match.group('username')
        return None
