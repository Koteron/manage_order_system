import logging
import sys

def setup_logging():
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        ch.setFormatter(formatter)

        logger.addHandler(ch)