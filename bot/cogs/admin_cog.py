from tortoise.expressions import F
from twitchio.ext import commands

from bot.cogs.base import BaseCog
from bot.config import DEV_NICK
from db import FishingStats, FishingLogs, RandomPingStats
from logs import logger


class AdminCog(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.command()
    async def rename(self, ctx: commands.Context, *args: str):
        from_username, to_username = args

        if ctx.message.author.name.lower() == DEV_NICK:
            from_angler = await FishingStats.get(fisherman=from_username)
            to_angler, _ = await FishingStats.get_or_create(fisherman=to_username)
            to_angler.casts = F('casts') + from_angler.casts
            to_angler.snaps = F('snaps') + from_angler.snaps
            await to_angler.save()
            await from_angler.delete()

            await FishingLogs.filter(fisherman=from_username).update(fisherman=to_username)
            await FishingLogs.filter(fish=from_username).update(fish=to_username)

            from_user = await RandomPingStats.get(username=from_username)
            to_user, _ = await RandomPingStats.get_or_create(username=from_username)
            to_user.random_pings = F('random_pings') + from_user.random_pings
            to_user.times_pinged = F('times_pinged') + from_user.times_pinged
            await to_user.save()
            await from_user.delete()

            await ctx.send(f'{from_username} updated to {to_username}')
            logger.info(f'{from_username} updated to {to_username}')
        else:
            await ctx.send(f'You don\'t have permission to use this command')
