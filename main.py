from dotenv import load_dotenv

load_dotenv()  # should happen first, even before imports

if __name__ == '__main__':
    import db
    from bot import yepp_bot
    from logs import logger

    try:
        yepp_bot.loop.run_until_complete(db.init())
        yepp_bot.loop.run_until_complete(yepp_bot.connect())
        yepp_bot.loop.run_forever()
    except Exception as exc:
        logger.critical(exc, exc_info=1)
        yepp_bot.loop.run_until_complete(db.close())
    else:
        yepp_bot.loop.run_until_complete(db.close())
    finally:
        yepp_bot.loop.run_until_complete(yepp_bot.close())
        yepp_bot.loop.close()
