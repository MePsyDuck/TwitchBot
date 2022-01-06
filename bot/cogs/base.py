import re

from twitchio.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def get_user_from_mention(ctx: commands.Context, *args: str):
        username = ctx.author.name.lower()

        if args and len(args) == 1:
            tmp_uname = args[0].lower().strip()
            if args[0].startswith('@'):
                tmp_uname = tmp_uname[1:]

            if re.match(r'^[a-zA-Z0-9_]{4,25}$', tmp_uname):
                username = tmp_uname

        return username
