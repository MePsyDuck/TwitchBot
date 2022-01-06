import re

from tortoise.expressions import F
from twitchio import Message
from twitchio.ext import commands

from db import FishingStats


class FishingStatsCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.event()
    async def event_message(self, message: Message):
        if message.echo:
            return

        if message.author.name.lower() == 'skwishi':
            if match := re.search(r'(?P<username>[a-zA-Z0-9_]{4,25}) has snapped their line and got nothing. Try again later', message.content):
                fisherman = match.group('username').lower()

                fisherman_stats, _ = await FishingStats.get_or_create(username=fisherman)
                fisherman_stats.snaps = F('snaps') + 1
                await fisherman_stats.save()

                print(f'{fisherman} snapped')

            elif match := re.search(r'(?P<username>[a-zA-Z0-9_]{4,25}) has caught a fish called the '
                                    r'(?P<fish>[a-zA-Z0-9_]{4,25}) for '
                                    r'(?P<points>[0-9]+) angler points. OOOO', message.content):
                fisherman = match.group('username').lower()
                fish = match.group('fish').lower()
                points = match.group('points')

                fisherman_stats, _ = await FishingStats.get_or_create(username=fisherman)
                fisherman_stats.catches = F('catches') + 1
                fisherman_stats.biggest_catch = max(fisherman_stats.biggest_catch, points)
                await fisherman_stats.save()

                fish_stats, _ = await FishingStats.get_or_create(username=fish)
                fish_stats.times_caught = F('times_caught') + 1

                await fish_stats.save()

                print(f'{fisherman} caught {fish} for {points} points')

        elif re.search(r'!cast(.*)', message.content):
            fisherman = message.author.name.lower()

            fisherman_stats, _ = await FishingStats.get_or_create(username=fisherman)
            fisherman_stats.casts = F('casts') + 1
            await fisherman_stats.save()

            print(f'{fisherman} tried casting')

    @commands.command()
    @commands.cooldown(rate=1, per=60, bucket=commands.Bucket.default)
    async def fishingstats(self, ctx: commands.Context):
        if stats := await FishingStats.get_or_none(username=ctx.author.name.lower()):
            await ctx.send(f'{ctx.author.name} : casts={stats.casts}, snaps={stats.snaps}, catches={stats.catches}, '
                           f'biggest_catch={stats.biggest_catch}, times_caught={stats.times_caught}')
        else:
            await ctx.send(f'{ctx.author.name} has no fishing stats recorded.')
