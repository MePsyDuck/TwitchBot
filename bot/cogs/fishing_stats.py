import re

from tortoise.expressions import F
from twitchio import Message
from twitchio.ext import commands

from bot.cogs.base import BaseCog
from bot.config import COOLDOWN
from db import FishingStats, FishingLogs
from logs import logger


class FishingStatsCog(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.Cog.event()
    async def event_message(self, message: Message):
        if message.echo:
            return

        if message.author.name.lower() == 'skwishi' or message.author.name.lower() == self.bot.nick:
            if match := re.search(r'(?P<username>[a-zA-Z0-9_]{4,25}) has snapped their line and got nothing. Try again later', message.content):
                fisherman = match.group('username').lower()

                logger.debug(f'{fisherman} snapped')

                fisherman_stats, _ = await FishingStats.get_or_create(fisherman=fisherman)
                fisherman_stats.snaps = F('snaps') + 1
                await fisherman_stats.save()
            elif match := re.search(r'(?P<username>[a-zA-Z0-9_]{4,25}) has caught a (new species of )?fish called the '
                                    r'(?P<fish>[a-zA-Z0-9_]{4,25}) (for|worth) '
                                    r'(?P<points>[0-9]+) (angler )?points. OOOO', message.content):
                fisherman = match.group('username').lower()
                fish = match.group('fish').lower()
                points = int(match.group('points'))

                logger.debug(f'{fisherman} caught {fish} for {points} points')
                await FishingLogs.create(fisherman=fisherman, fish=fish, points=points)

        elif re.search(r'!cast(.*)', message.content):
            fisherman = message.author.name.lower()

            logger.debug(f'{fisherman} tried casting')

            fisherman_stats, _ = await FishingStats.get_or_create(fisherman=fisherman)
            fisherman_stats.casts = F('casts') + 1
            await fisherman_stats.save()

    @commands.command(aliases=['fs'])
    @commands.cooldown(rate=1, per=COOLDOWN, bucket=commands.Bucket.default)
    async def fishingstats(self, ctx: commands.Context, *args: str):
        username = self.get_user_from_mention(ctx, *args)

        if stats := await FishingStats.get_or_none(fisherman=username):
            times_caught = await FishingLogs.filter(fish=username).count()
            catches = await FishingLogs.filter(fisherman=username).count()
            biggest_catch = ''
            if catches > 0:
                biggest_catch = await FishingLogs.filter(fisherman=username).order_by('-points', '-when').first()
                biggest_catch = f'biggest fish {biggest_catch.fish}({biggest_catch.points}), '
            await ctx.send(
                f'{username} {stats.snaps + catches} casts, {stats.snaps} snaps ({stats.snaps * 100 // (stats.snaps + catches)}%), {catches} catches, '
                f'{biggest_catch}caught {times_caught} times.')
        else:
            await ctx.send(f'{username} has no fishing stats recorded.')

    @commands.command(aliases=['snappers'])
    @commands.cooldown(rate=1, per=COOLDOWN, bucket=commands.Bucket.default)
    async def topsnappers(self, ctx: commands.Context):
        top_snappers = await FishingStats.all().order_by('-snaps', '-casts').limit(7)
        await ctx.send(f'x0r6ztGiggle {", ".join([f"{snapper.fisherman} {snapper.snaps}" for snapper in top_snappers])}')
