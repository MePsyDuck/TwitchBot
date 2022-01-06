import os

DEBUG = os.getenv('DEBUG', 'False') == 'True'
BOT_LOGGER = 'bot'
LOG_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO').upper()
LOG_FORMAT = '%(asctime)s %(levelname)-8s %(funcName)-25s %(message)s'
LOG_FILENAME = 'bot.log'
