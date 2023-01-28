import logging

from twitchio import Message
from twitchio.ext import commands

from bot.cogs.base import BaseCog


class ChatLoggingCog(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        file_handler = logging.FileHandler('chat.log', mode='a', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        file_handler.setLevel(logging.INFO)
        self.logger = logging.getLogger('chat')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)

    @commands.Cog.event()
    async def event_message(self, message: Message):
        if message.channel.name == 'singsing':
            self.logger.info(f'{message.timestamp} {message.author.name if message.author else ""} : {message.content}')
