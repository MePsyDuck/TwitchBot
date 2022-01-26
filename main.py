from dotenv import load_dotenv

load_dotenv()  # should happen first, even before imports

if __name__ == '__main__':
    import db
    from bot import YeppBot
    from logs import logger

    bot = YeppBot()

    try:
        bot.loop.run_until_complete(db.init())
        bot.loop.run_until_complete(bot.connect())
        bot.loop.run_forever()
    except Exception as exc:
        logger.critical(exc, exc_info=1)
        bot.loop.run_until_complete(db.close())
    else:
        bot.loop.run_until_complete(db.close())
    finally:
        bot.loop.run_until_complete(bot.close())
        bot.loop.close()
