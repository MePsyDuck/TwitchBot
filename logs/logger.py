import logging

from logs.config import BOT_LOGGER, LOG_FORMAT, LOG_LEVEL, BOT_LOG_FILENAME, DEBUG, ROOT_LOG_FILENAME

logger = logging.getLogger(BOT_LOGGER)


def setup_logger():
    log_formatter = logging.Formatter(LOG_FORMAT)
    log_level = logging.getLevelName(LOG_LEVEL)

    # Root logging
    file_handler = logging.FileHandler(ROOT_LOG_FILENAME, mode='a')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)

    default_logger = logging.getLogger()
    default_logger.setLevel(log_level)
    default_logger.addHandler(file_handler)

    # Bot logging
    file_handler = logging.FileHandler(BOT_LOG_FILENAME, mode='a')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)

    bot_logger = logging.getLogger(BOT_LOGGER)
    bot_logger.setLevel(log_level)
    bot_logger.addHandler(file_handler)

    if DEBUG:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        stream_handler.setLevel(logging.DEBUG)

        bot_logger.addHandler(stream_handler)
        default_logger.addHandler(stream_handler)
