import re

from tortoise.expressions import F
from twitchio import Message
from twitchio.ext import commands

from bot.cogs.base import BaseCog
from bot.config import COOLDOWN
from db import ShootoutStats
from logs import logger


class LastDuel:
    shooter = None
    user_shot = None

    def update(self, shooter, user_shot):
        self.shooter = shooter
        self.user_shot = user_shot


class ShootoutStatsCog(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        self.last_duel = LastDuel()

    @commands.Cog.event()
    async def event_message(self, message: Message):
        if message.echo:
            return

        if message.author.name.lower() == 'skwishi':
            if match := re.search(r'(?P<loser>\S+) has lost this round', message.content):
                loser = match.group('loser').lower()
                winner = 'unknown'

                if loser in [self.last_duel.shooter, self.last_duel.user_shot]:
                    winner = self.last_duel.shooter if self.last_duel.user_shot == loser else self.last_duel.shooter
                    winner_stats, _ = await ShootoutStats.get_or_create(username=winner)
                    if winner_stats.highest_win_streak == winner_stats.current_win_streak:
                        winner_stats.highest_win_streak = F('highest_win_streak') + 1
                    winner_stats.current_win_streak = F('current_win_streak') + 1
                    winner_stats.current_loss_streak = 0
                    await winner_stats.save()

                loser_stats, _ = await ShootoutStats.get_or_create(username=loser)
                if loser_stats.highest_loss_streak == loser_stats.current_loss_streak:
                    loser_stats.highest_loss_streak = F('highest_loss_streak') + 1
                loser_stats.current_loss_streak = F('current_loss_streak') + 1
                loser_stats.current_win_streak = 0
                await loser_stats.save()

                logger.info(f'{loser} lost shootout against {winner}')

        elif match := re.search(r'!shootout (?P<user_shot>\S+)( .*)?', message.content):
            shooter = message.author.name.lower()

            shooter_stats, _ = await ShootoutStats.get_or_create(username=shooter)
            shooter_stats.duels_started = F('duels_started') + 1
            await shooter_stats.save()

            user_shot = match.group('user_shot').lower()
            user_stats, _ = await ShootoutStats.get_or_create(username=user_shot)
            user_stats.duels_accepted = F('duels_accepted') + 1
            await user_stats.save()

            logger.info(f'{shooter} dueled {user_shot}')

            self.last_duel.update(shooter, user_shot)

    @commands.command(aliases=['ss'])
    @commands.cooldown(rate=1, per=COOLDOWN, bucket=commands.Bucket.default)
    async def shootoutstats(self, ctx: commands.Context, *args: str):
        username = self.get_mentioned_user(*args) or ctx.author.name
        username_lower = username.lower()

        if stats := await ShootoutStats.get_or_none(username=username_lower):
            await ctx.send(
                f'{username} losses={stats.current_loss_streak}/{stats.highest_loss_streak}, '
                f'wins={stats.current_win_streak}/{stats.highest_win_streak},')
        else:
            await ctx.send(f'{username} has no stats')
