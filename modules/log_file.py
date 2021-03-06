import os, sys, tempfile
import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = os.path.join(tempfile.gettempdir(), "Natur.log")
LOG_LEVEL = logging.DEBUG


class CustomFormatter(logging.Formatter):
    """See https://gist.github.com/abritinthebay/d80eb99b2726c83feb0d97eab95206c4"""

    reset = "\x1b[0m"
    fmt = "{}[%(levelname)s]{}\t[{origin}] %(message)s"
    origin = "\x1b[;3m%(name)s (%(funcName)s)\x1b[0m"

    FORMATS = {
        logging.DEBUG: "\x1b[;1m",
        logging.INFO: "\x1b[32m",
        logging.WARNING: "\x1b[33m",
        logging.ERROR: "\x1b[31m",
        logging.CRITICAL: "\x1b[31;1m",
    }

    def format(self, record):
        ori = self.origin
        fmt = self.fmt
        if "__main__" in record.name:
            ori = "\x1b[;3mCore\x1b[0m"
        log_fmt = fmt.format(self.FORMATS.get(record.levelno), self.reset, origin=ori)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


FORMATTER = CustomFormatter()
FORMATTER_FILE = logging.Formatter("%(asctime)s [ %(levelname)s ]\t %(message)s")


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = RotatingFileHandler(LOG_FILE, backupCount=1, maxBytes=1e5)
    file_handler.setFormatter(FORMATTER_FILE)
    return file_handler


def getLog(logger_name, level=LOG_LEVEL, file=True, console=True, name_is_file=False):
    if name_is_file:
        logger_name = os.path.basename(logger_name)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    if console:
        logger.addHandler(get_console_handler())
    if file:
        logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
