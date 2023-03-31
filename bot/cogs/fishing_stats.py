import re
import random

from cacheout import LRUCache
from regex import regex
from tortoise.expressions import F
from tortoise.functions import Count
from twitchio import Message
from twitchio.ext import commands

from bot.cogs.base import BaseCog
from bot.config import COOLDOWN, DEV_NICK
from db import FishingStats, FishingLogs
from logs import logger


class LastSnapper:
    username = ''
    snaps = 0

    def add_snap(self, username):
        if self.username == username:
            self.snaps += 1
        else:
            self.username = username
            self.snaps = 1

    def reset(self):
        self.username = ''
        self.snaps = 0


class FishingStatsCog(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        self.cache = LRUCache()
        self.last_snapper = LastSnapper()

    @commands.Cog.event()
    async def event_message(self, message: Message):
        if message.echo:
            return

        if message.author.name.lower() == 'skwishi' or message.author.name.lower() == DEV_NICK:
            if match := regex.search(r'(?P<display_name>[\p{L}|\p{N}_]+) has snapped their line and got nothing. Try '
                                     r'again later', message.content):
                display_name = match.group('display_name').lower()
                if not re.match(r'[a-z0-9_]{4,25}', display_name):
                    if self.cache.get(display_name):
                        fisherman = self.cache.get(display_name)
                    else:
                        logger.critical(f'{display_name} not in cache, {message.author.name.lower()}: {message.content}')
                        return
                else:
                    fisherman = display_name

                fisherman_stats, _ = await FishingStats.get_or_create(fisherman=fisherman)
                fisherman_stats.snaps = F('snaps') + 1
                await fisherman_stats.save()

                self.last_snapper.add_snap(fisherman)
                if self.last_snapper.snaps >= 5:
                    await message.channel.send(random.choice(['WEIRD', 'FeelsWeirdestMan', 'peepoWeirdClap', 'WeirdEyes', 'weirdPaper',
                                            'Weirdga', 'x0r6ztGiggle', 'ElNoSabe', 'Shirley', 'Clueless', 'singWeird', 'WeirdChamp',
                                            'CouldYouNot', 'getHelp']))

                logger.info(f'{fisherman} snapped')

            elif match := regex.search(r'(?P<display_name>[\p{L}|\p{N}_]+) has caught a (new species of )?fish '
                                       r'called the (?P<fish>[a-zA-Z0-9_]{4,25}) (for|worth) '
                                       r'(?P<points>[0-9]+) (angler )?points. OOOO', message.content):
                display_name = match.group('display_name').lower()
                if not re.match(r'[a-z0-9_]{4,25}', display_name):
                    if self.cache.get(display_name):
                        fisherman = self.cache.get(display_name)
                    else:
                        logger.critical(f'{display_name} not in cache, {message.author.name.lower()}: {message.content}')
                        return
                else:
                    fisherman = display_name

                fish = match.group('fish').lower()
                points = int(match.group('points'))
                await FishingLogs.create(fisherman=fisherman, fish=fish, points=points)

                logger.info(f'{fisherman} caught {fish} for {points} points')

                self.last_snapper.reset()

        elif re.search(r'!cast(.*)', message.content):
            fisherman = message.author.name.lower()

            if message.author.display_name.lower() != fisherman:
                self.cache.set(message.author.display_name.lower(), fisherman)

            fisherman_stats, _ = await FishingStats.get_or_create(fisherman=fisherman)
            fisherman_stats.casts = F('casts') + 1
            await fisherman_stats.save()

            logger.info(f'{fisherman} tried casting')

    @commands.command(aliases=['fs'])
    @commands.cooldown(rate=1, per=COOLDOWN, bucket=commands.Bucket.default)
    async def fishingstats(self, ctx: commands.Context, *args: str):
        username = self.get_mentioned_user(*args) or ctx.author.name
        username_lower = username.lower()

        if stats := await FishingStats.get_or_none(fisherman=username_lower):
            times_caught = await FishingLogs.filter(fish=username_lower).count()
            catches = await FishingLogs.filter(fisherman=username_lower).count()

            biggest_catch = None
            biggest_fish = None
            if catches > 0:
                biggest_catch = await FishingLogs.filter(fisherman=username_lower).order_by('-points', '-when').first()
                biggest_fish = biggest_catch.fish if biggest_catch.fish != 'auloen' else 'gachiGOLD '

            casts = stats.snaps + catches

            percent = stats.snaps * 100 // casts
            if username_lower == 'king_of_evi1':
                percent = 50.00

            if casts > 0:
                await ctx.send(
                    f'{username} {casts} casts, '
                    f'{stats.snaps} snaps ({percent}%), '
                    f'{catches} caught, '
                    f'{f"biggest fish {biggest_fish}({biggest_catch.points}), " if biggest_catch else ""}'
                    f'{f"caught {times_caught} times" if times_caught else "never caught"}'
                )
            else:
                await ctx.send(f'{username} has no fishing stats recorded.')
        else:
            await ctx.send(f'{username} has no fishing stats recorded.')

    @commands.command(aliases=['snappers'])
    @commands.cooldown(rate=1, per=COOLDOWN, bucket=commands.Bucket.default)
    async def topsnappers(self, ctx: commands.Context):
        top_snappers = await FishingStats.all().order_by('-snaps', '-casts').limit(5)
        await ctx.send(f'x0r6ztGiggle {", ".join([f"{snapper.fisherman} {snapper.snaps}" for snapper in top_snappers])}')

    @commands.command(aliases=['catches'])
    @commands.cooldown(rate=1, per=COOLDOWN, bucket=commands.Bucket.default)
    async def topcatches(self, ctx: commands.Context):
        top_catchers = await FishingLogs.annotate(count=Count('id')).group_by('fisherman').order_by('-count')\
            .limit(5).values('fisherman', 'count')
        await ctx.send('🎣 ' + ', '.join([f"{catcher['fisherman']} {catcher['count']}" for catcher in top_catchers]))

    @commands.command(aliases=['caught'])
    @commands.cooldown(rate=1, per=COOLDOWN, bucket=commands.Bucket.default)
    async def topcaught(self, ctx: commands.Context):
        top_caught = await FishingLogs.annotate(count=Count('id')).group_by('fish').order_by('-count')\
            .limit(5).values('fish', 'count')
        await ctx.send('FailFish ' + ', '.join([f"{fish['fish']} {fish['count']}" for fish in top_caught]))
