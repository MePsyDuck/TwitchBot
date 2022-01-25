import asyncio
import re

from twitchio.ext import commands

from bot.config import SELF_REPLY_DELAY


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        print(ctx.author.badges)
        if ctx.author.name == ctx.bot.nick:
            if not any(badge in ctx.author.badges for badge in ['vip', 'moderator', 'broadcaster']):
                await asyncio.sleep(SELF_REPLY_DELAY)
        return True

    @staticmethod
    def get_user_from_mention(ctx: commands.Context, *args: str):
        username = ctx.author.name.lower()

        if args and len(args) == 1:
            tmp_uname = args[0].lower().strip()
            if args[0].startswith('@'):
                tmp_uname = tmp_uname[1:]

            if re.match(r'^[a-zA-Z0-9_]{4,25}$', tmp_uname):
                username = tmp_uname

        return username
