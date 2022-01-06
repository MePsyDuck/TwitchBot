import logging

from logs.config import BOT_LOGGER, LOG_FORMAT, LOG_LEVEL, LOG_FILENAME, DEBUG

logger = logging.getLogger(BOT_LOGGER)


def setup_logger():
    log_formatter = logging.Formatter(LOG_FORMAT)
    log_level = logging.getLevelName(LOG_LEVEL)

    # Handlers
    file_handler = logging.FileHandler(LOG_FILENAME, mode='a')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    # Internal logging
    bot_logger = logging.getLogger(BOT_LOGGER)
    bot_logger.setLevel(log_level)
    bot_logger.addHandler(file_handler)

    if DEBUG:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        stream_handler.setLevel(logging.DEBUG)

        bot_logger.addHandler(stream_handler)
