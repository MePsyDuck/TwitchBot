import re

from tortoise.expressions import F
from twitchio import Message
from twitchio.ext import commands

from db import RandomPingStats


class RandomPingStatsCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

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

                print(f'pinged: {pinged_users}')

        elif re.search('!randomping(.*)', message.content):
            user = message.author.name.lower()

            ping_stats, _ = await RandomPingStats.get_or_create(username=user)
            ping_stats.random_pings = F('random_pings') + 1
            await ping_stats.save()

            print(f'{user} randompinged')

    @commands.command(aliases=['pingstats'])
    @commands.cooldown(rate=1, per=60, bucket=commands.Bucket.default)
    async def randompingstats(self, ctx: commands.Context):
        if stats := await RandomPingStats.get_or_none(username=ctx.author.name.lower()):
            await ctx.send(f'{ctx.author.name} was pinged {stats.times_pinged} times')
        else:
            await ctx.send(f'{ctx.author.name} was never pinged')
