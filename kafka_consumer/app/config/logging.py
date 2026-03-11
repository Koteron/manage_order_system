"""
Structured Application Logging Configuration.

Initializes the 'app' logger used throughout the system. Standardizes 
the output format for console/container logs to simplify debugging 
and log aggregation (e.g., ELK or CloudWatch).
"""
import logging
import sys

async def setup_logging():
    """
    Configures a centralized stream logger for the application.

    Initializes the 'app' logger at the DEBUG level and attaches a 
    StreamHandler pointing to stdout. 

    Features:
    - **Idempotency Check**: Uses 'hasHandlers()' to ensure handlers 
      are not duplicated if the function is called multiple times 
      (common during FastAPI hot-reloads).
    - **Custom Formatting**: Includes timestamps, log levels, and 
      logger names for improved traceability.
    - **Output Stream**: Directs all logs to 'sys.stdout' for 
      compatibility with Docker/Kubernetes log collectors.

    Format Example:
        [2026-03-11 12:00:00] [INFO] [app] Created order with id: 1
    """
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