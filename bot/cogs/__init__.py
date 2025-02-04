from .admin_cog import AdminCog
from .chat_log import ChatLoggingCog
from .fishing_stats import FishingStatsCog
from .random_ping_stats import RandomPingStatsCog
from .roll_stats import RollStatsCog
from .shootout_stats import ShootoutStatsCog


def prepare(bot):
    bot.add_cog(AdminCog(bot))
    bot.add_cog(ChatLoggingCog(bot))
    bot.add_cog(FishingStatsCog(bot))
    bot.add_cog(RandomPingStatsCog(bot))
    bot.add_cog(RollStatsCog(bot))
    bot.add_cog(ShootoutStatsCog(bot))
