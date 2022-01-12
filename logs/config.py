import os

DEBUG = os.getenv('DEBUG', 'False') == 'True'
BOT_LOGGER = 'bot'
LOG_LEVEL = 'DEBUG' if DEBUG else os.environ.get('LOGGING_LEVEL', 'INFO').upper()
LOG_FORMAT = '%(asctime)s %(levelname)-8s %(name)-25s %(funcName)-25s %(message)s'
BOT_LOG_FILENAME = 'bot.log'
ROOT_LOG_FILENAME = 'app.log'
