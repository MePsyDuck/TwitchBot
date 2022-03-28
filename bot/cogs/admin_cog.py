from twitchio.ext import commands

from bot.cogs.base import BaseCog
from bot.config import DEV_NICK
from db import FishingStats, FishingLogs, RandomPingStats
from logs import logger


class FAdminsCog(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.command()
    async def rename(self, ctx: commands.Context, *args: str):
        from_username, to_username = args

        if ctx.message.author.name.lower() == DEV_NICK:
            await FishingStats.filter(fisherman=from_username).update(fisherman=to_username)
            await FishingLogs.filter(fisherman=from_username).update(fisherman=to_username)
            await FishingLogs.filter(fish=from_username).update(fish=to_username)
            await RandomPingStats.filter(username=from_username).update(username=to_username)
            await ctx.send(f'{from_username} updated to {to_username}')
            logger.info(f'{from_username} updated to {to_username}')
        else:
            await ctx.send(f'You don\'t have permission to use this command')
