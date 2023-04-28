from logging import Logger, StreamHandler, Formatter
import sys
import logging


def get_logger(log_level) -> Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    log_handler = StreamHandler(stream=sys.stdout)
    log_handler.setFormatter(Formatter(fmt="%(asctime)s: %(levelname)s %(message)s"))
    logger.addHandler(log_handler)

    return logger
