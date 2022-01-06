from dotenv import load_dotenv

import db
from logs.logger import setup_logger

load_dotenv()
setup_logger()

if __name__ == '__main__':
    from bot.yepp_bot import YeppBot

    bot = YeppBot()

    try:
        bot.loop.run_until_complete(db.init())
        bot.loop.run_until_complete(bot.connect())
        bot.loop.run_forever()
    except:
        bot.loop.run_until_complete(db.close())
    else:
        bot.loop.run_until_complete(db.close())
    finally:
        bot.loop.run_until_complete(bot.close())
        bot.loop.close()
