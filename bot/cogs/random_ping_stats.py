import re

from tortoise.expressions import F
from twitchio import Message
from twitchio.ext import commands

from bot.cogs.base import BaseCog
from bot.config import COOLDOWN
from db import RandomPingStats
from logs.logger import logger


class RandomPingStatsCog(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.Cog.event()
    async def event_message(self, message: Message):
        if message.echo:
            return

        if message.author.name.lower() == 'skwishi':
            if match := re.search(r'DinkDonk (?P<users>([a-zA-Z0-9_]{4,25}\s?)+)', message.content):
                pinged_users = match.group('users').lower()

                for user in re.findall(r'([a-zA-Z0-9_]{4,25})\s?', pinged_users):
                    ping_stats, _ = await RandomPingStats.get_or_create(username=user)
                    ping_stats.times_pinged = F('times_pinged') + 1
                    await ping_stats.save()

                logger.debug(f'pinged: {pinged_users}')

        elif re.search('!randomping(.*)', message.content):
            user = message.author.name.lower()

            ping_stats, _ = await RandomPingStats.get_or_create(username=user)
            ping_stats.random_pings = F('random_pings') + 1
            await ping_stats.save()

            logger.debug(f'{user} randompinged')

    @commands.command(aliases=['ps'])
    @commands.cooldown(rate=1, per=COOLDOWN, bucket=commands.Bucket.default)
    async def randompingstats(self, ctx: commands.Context, *args: str):
        username = self.get_user_from_mention(ctx, *args)

        if stats := await RandomPingStats.get_or_none(username=username):
            await ctx.send(f'{username} was pinged {stats.times_pinged} times')
        else:
            await ctx.send(f'{username} was never pinged')