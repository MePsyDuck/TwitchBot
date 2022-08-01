import re

from twitchio.ext import commands, eventsub

from bot.config import CLIENT_ID, CLIENT_SECRET, WEBHOOK_SECRET, CALLBACK_URL, LISTEN_PORT
from logs import logger

bot_client = commands.Bot.from_client_credentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
eventsub_client = eventsub.EventSubClient(client=bot_client, webhook_secret=WEBHOOK_SECRET, callback_route=CALLBACK_URL)


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.loop.create_task(eventsub_client.listen(port=LISTEN_PORT))

    async def cog_command_error(self, ctx: commands.Context, exc: Exception):
        logger.error(exc, exc_info=True)

    @staticmethod
    def get_mentioned_user(*args: str):
        if args:
            if match := re.search(r'\s*@?(?P<username>[a-zA-Z0-9_]{4,25}),?\s*', args[0]):
                return match.group('username')
        return None
