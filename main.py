from dotenv import load_dotenv

load_dotenv()  # should happen first, even before imports

if __name__ == '__main__':
    import db
    from bot.yepp_bot import YeppBot
    from logs.logger import setup_logger

    setup_logger()

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
