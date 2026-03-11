"""
Structured Application Logging Configuration.

Initializes the 'app' logger used throughout the system. Standardizes 
the output format for console/container logs to simplify debugging 
and log aggregation (e.g., ELK or CloudWatch).
"""
import logging
import sys

async def setup_logging():
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