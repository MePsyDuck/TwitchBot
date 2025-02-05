from regex import regex
from tortoise.expressions import F
from twitchio import Message
from twitchio.ext import commands

from bot.cogs.base import BaseCog
from bot.config import DEV_NICK
from db import RollLogs, RollStats
from logs import logger


class RollStatsCog(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.Cog.event()
    async def event_message(self, message: Message):
        if message.echo:
            return

        if message.author.name.lower() == 'skwishi' or message.author.name.lower() == DEV_NICK:
            if match := regex.search(r'(?P<display_name>[\p{L}|\p{N}_]+) has rolled a (?P<roll>([0-9]+|Nat1|Nat20))',
                                     message.content):
                username = match.group('display_name').lower()
                roll = match.group('roll')

                if roll == 'Nat1':
                    roll_value = 1
                elif roll == 'Nat20':
                    roll_value = 20
                else:
                    roll_value = int(roll)

                await RollLogs.create(username=username, rolled_value=roll_value)

                logger.info(f'{username} rolled {roll}')

        if message.content.startswith('!roll'):
            username = message.author.name.lower()

            roll_stats, _ = await RollStats.get_or_create(username=username)
            roll_stats.rolls = F('rolls') + 1
            await roll_stats.save()

            logger.info(f'{username} tried rolling')

# TODO add commands for stats
