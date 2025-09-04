"""Logging configuration module for the most active cookie finder."""

import logging
from typing import Optional


def setup_logging(
    verbose: bool = False, logger_name: Optional[str] = None
) -> logging.Logger:
    """Setup logging configuration.

    Args:
        verbose: Enable verbose (DEBUG) logging if True, otherwise WARNING level
        logger_name: Name of the logger, defaults to calling module name

    Returns:
        Configured logger instance
    """
    log_level = logging.DEBUG if verbose else logging.WARNING

    # Configure the root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        force=True,  # Override any existing configuration
    )

    # Get logger for the specific module
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with current global configuration.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance using global configuration
    """
    return logging.getLogger(name)
