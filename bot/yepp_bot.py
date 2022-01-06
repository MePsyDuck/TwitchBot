from twitchio.ext import commands

from bot.cogs import FishingStatsCog, RandomPingStatsCog
from bot.config import ACCESS_TOKEN, CHANNELS, PREFIX


class YeppBot(commands.Bot):

    def __init__(self):
        super().__init__(token=ACCESS_TOKEN, prefix=PREFIX, initial_channels=CHANNELS)
        self.add_cog(FishingStatsCog(self))
        self.add_cog(RandomPingStatsCog(self))

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
