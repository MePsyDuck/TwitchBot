from dotenv import load_dotenv

from bot.cogs.FishingStats import FishingStats

load_dotenv()

if __name__ == '__main__':
    from bot.yepp_bot import YeppBot

    bot = YeppBot()
    bot.add_cog(FishingStats(bot))
    bot.run()
