import re

from tortoise.expressions import F
from twitchio import Message
from twitchio.ext import commands

from bot.cogs.base import BaseCog
from bot.config import COOLDOWN
from db import ShootoutLogs, ShootoutStats
from logs import logger


class LastDuel:
    challenger = None
    target = None

    def update(self, challenger, target):
        self.challenger = challenger
        self.target = target

    def get_winner(self, loser):
        return self.challenger if self.target == loser else self.target


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

                if loser in [self.last_duel.challenger, self.last_duel.target]:
                    winner = self.last_duel.get_winner(loser)
                    winner_stats, _ = await ShootoutStats.get_or_create(username=winner)
                    if winner_stats.highest_win_streak == winner_stats.current_win_streak:
                        winner_stats.highest_win_streak = F('highest_win_streak') + 1
                    winner_stats.current_win_streak = F('current_win_streak') + 1
                    winner_stats.total_won = F('total_won') + 1
                    winner_stats.current_loss_streak = 0
                    await winner_stats.save()
                else:
                    logger.critical(f'{loser} not in last duel : {self.last_duel.challenger}, {self.last_duel.target}')

                loser_stats, _ = await ShootoutStats.get_or_create(username=loser)
                if loser_stats.highest_loss_streak == loser_stats.current_loss_streak:
                    loser_stats.highest_loss_streak = F('highest_loss_streak') + 1
                loser_stats.current_loss_streak = F('current_loss_streak') + 1
                loser_stats.current_win_streak = 0
                loser_stats.total_lost = F('total_lost') + 1
                await loser_stats.save()

                await ShootoutLogs.create(challenger=self.last_duel.challenger, target=self.last_duel.target, winner=winner, loser=loser)

                logger.info(f'{loser} lost shootout against {winner}')

        if match := re.search(r'!shootout (?P<target>\S+)( .{3+})?', message.content):
            challenger = message.author.name.lower()

            challenger_stats, _ = await ShootoutStats.get_or_create(username=challenger)
            challenger_stats.duels_started = F('duels_started') + 1
            await challenger_stats.save()

            target = self.get_mentioned_user(match.group('target')) or match.group('target')
            target = target.lower()
            target_stats, _ = await ShootoutStats.get_or_create(username=target)
            target_stats.duels_accepted = F('duels_accepted') + 1
            await target_stats.save()

            logger.info(f'{challenger} dueled {target}')

            self.last_duel.update(challenger, target)

    @commands.command(aliases=['ss'])
    @commands.cooldown(rate=1, per=COOLDOWN, bucket=commands.Bucket.default)
    async def shootoutstats(self, ctx: commands.Context, *args: str):
        username = self.get_mentioned_user(*args) or ctx.author.name
        username_lower = username.lower()

        if stats := await ShootoutStats.get_or_none(username=username_lower):
            await ctx.send(f'{stats}')
        else:
            await ctx.send(f'{username} has no stats')
