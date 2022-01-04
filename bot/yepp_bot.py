from twitchio.ext import commands

from bot.config import ACCESS_TOKEN, CHANNELS, PREFIX


class YeppBot(commands.Bot):

    def __init__(self):
        super().__init__(token=ACCESS_TOKEN, prefix=PREFIX, initial_channels=CHANNELS)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return

        print(message.content)

        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')
