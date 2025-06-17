"""Logger utility for FastAPI application with colored output."
# fastapi_e2e/src/utils/logger.py
"""

import logging

from colorlog import ColoredFormatter

from src.config.config import config


def get_logger(logger_name: str):
    """
    Create and configure a logger with colored output.
    Args:
        logger_name (str): Name of the logger.
        Returns:
        logging.Logger: Configured logger instance.
    """
    # Create a logger instance
    logger = logging.getLogger(logger_name)
    logger.setLevel(config.get_log_level() or logging.INFO)

    # Set up console handler for logging
    console_handler = logging.StreamHandler()

    # Define the log format with colors based on log level
    formatter = ColoredFormatter(
        fmt=(
            "%(log_color)s [%(levelname)s] -> "
            "[%(asctime)s]-[%(name)s]=[%(funcName)s] ->  %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
    # Set the formatter for the console handler
    console_handler.setFormatter(formatter)

    # Add handler to the logger
    logger.addHandler(console_handler)

    return logger
