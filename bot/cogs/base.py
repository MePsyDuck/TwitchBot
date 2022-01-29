import asyncio
import re

from twitchio.ext import commands

from bot.config import SELF_REPLY_DELAY
from logs import logger


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(self, ctx: commands.Context, exc: Exception):
        logger.error(exc, exc_info=True)

    async def cog_check(self, ctx: commands.Context):
        if ctx.author.name == ctx.bot.nick:
            if not any(badge in ctx.author.badges for badge in ['vip', 'moderator', 'broadcaster']):
                await asyncio.sleep(SELF_REPLY_DELAY)
        return True

    @staticmethod
    def get_mentioned_user(*args: str):
        if args:
            if match := re.search(r'\s*@?(?P<username>[a-zA-Z0-9_]{4,25}),?\s*', args[0]):
                return match.group('username')
        return None
