from .fishing_stats import FishingStatsCog
from .random_ping_stats import RandomPingStatsCog
from .admin_cog import AdminCog
from .chat_log import ChatLoggingCog
from .channel_info import ChannelInfoCog


def prepare(bot):
    bot.add_cog(FishingStatsCog(bot))
    bot.add_cog(RandomPingStatsCog(bot))
    bot.add_cog(AdminCog(bot))
    bot.add_cog(ChatLoggingCog(bot))
    bot.add_cog(ChannelInfoCog(bot))
