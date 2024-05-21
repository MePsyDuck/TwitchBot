from .fishing_stats import FishingStatsCog
from .random_ping_stats import RandomPingStatsCog
from .shootout_stats import ShootoutStatsCog
from .admin_cog import AdminCog
from .chat_log import ChatLoggingCog


def prepare(bot):
    bot.add_cog(FishingStatsCog(bot))
    bot.add_cog(RandomPingStatsCog(bot))
    bot.add_cog(ShootoutStatsCog(bot))
    bot.add_cog(AdminCog(bot))
    bot.add_cog(ChatLoggingCog(bot))
