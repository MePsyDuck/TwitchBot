import re

from tortoise.expressions import F
from twitchio import Message
from twitchio.ext import commands

from bot.cogs.base import BaseCog
from bot.config import COOLDOWN
from db import ShootoutStats
from logs import logger


class ShootoutStatsCog(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.Cog.event()
    async def event_message(self, message: Message):
        if message.echo:
            return

        if message.author.name.lower() == 'skwishi':
            if match := re.search(r'(?P<loser>\S+) has lost this round', message.content):
                loser = match.group('loser').lower()

                loser_stats, _ = await ShootoutStats.get_or_create(username=loser)
                if loser_stats.highest_streak == loser_stats.current_streak:
                    loser_stats.highest_streak = F('highest_streak') + 1
                loser_stats.current_streak = F('current_streak') + 1
                await loser_stats.save()

                logger.info(f'{loser} lost shootout')

        elif match := re.search(r'!shootout (?P<user_shot>\S+) .*', message.content):
            shooter = message.author.name.lower()

            shooter_stats, _ = await ShootoutStats.get_or_create(username=shooter)
            shooter_stats.duels_started = F('duels_started') + 1
            await shooter_stats.save()

            user_shot = match.group('user_shot').lower()
            user_stats, _ = await ShootoutStats.get_or_create(username=user_shot)
            user_stats.duels_accepted = F('duels_accepted') + 1
            await user_stats.save()

            logger.info(f'{shooter} dueled {user_shot}')

    @commands.command(aliases=['ss'])
    @commands.cooldown(rate=1, per=COOLDOWN, bucket=commands.Bucket.default)
    async def shootoutstats(self, ctx: commands.Context, *args: str):
        username = self.get_mentioned_user(*args) or ctx.author.name
        username_lower = username.lower()

        if stats := await ShootoutStats.get_or_none(username=username_lower):
            await ctx.send(f'{username} is on {stats.current_streak} loss streak, highest loss streak {stats.highest_streak}')
        else:
            await ctx.send(f'{username} was never shot at')
