import re

from twitchio import Message
from twitchio.ext import commands

from db.db_api import db_api


class FishingStats(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.event()
    async def event_message(self, message: Message):
        if message.echo:
            return

        if message.author.name.lower() == 'skwishi':
            if match := re.search('(?P<username>[a-zA-Z0-9_]{4,25}) has snapped their line and got nothing. Try again later', message.content):
                db_api.update_for_snaps(username=match.group('username'))
                print(f'{match.group("username")} snapped')
            elif match := re.search('(?P<username>[a-zA-Z0-9_]{4,25}) has caught a fish called the (?P<fish>[a-zA-Z0-9_]{4,25}) for (?P<points>[0-9]+) angler '
                                    'points. OOOO',
                                    message.content):
                db_api.update_for_catch(username=match.group('username'), fish=match.group('fish'), points=match.group('points'))
        else:
            if re.search('!cast(.*)', message.content):
                db_api.update_casts(username=message.author.name)

    @commands.command()
    async def stats(self, ctx: commands.Context):
        stats = db_api.get_fishing_stats(ctx.author.name)
        await ctx.send(f'{ctx.author.name} : casts={stats.casts}, snaps={stats.snaps}, catches={stats.catches}, biggest_catch='
                       f'{stats.biggest_catch}, times_caught={stats.times_caught}')
