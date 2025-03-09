# src/utilities/custom_logger.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import allure

class CustomLogger:
    # Default log directory
    LOG_DIR = Path("./logs")
    DEFAULT_LOG_FILE = LOG_DIR / "appium_framework.log"

    @staticmethod
    def ensure_log_directory():
        """Ensure the log directory exists."""
        if not CustomLogger.LOG_DIR.exists():
            CustomLogger.LOG_DIR.mkdir(parents=True)

    @staticmethod
    def get_logger(name, level=logging.INFO, log_to_file=True, max_bytes=10485760, backup_count=5):
        """
        Configure and return a logger instance.

        Args:
            name: Name of the logger (typically __name__)
            level: Logging level (default: INFO)
            log_to_file: Whether to log to a file (default: True)
            max_bytes: Max size of log file before rotation (default: 10MB)
            backup_count: Number of backup files to keep (default: 5)
        """
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Avoid adding handlers if they already exist
        if logger.handlers:
            return logger

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler with rotation
        if log_to_file:
            CustomLogger.ensure_log_directory()
            file_handler = RotatingFileHandler(
                filename=CustomLogger.DEFAULT_LOG_FILE,
                maxBytes=max_bytes,  # Rotate after 10MB
                backupCount=backup_count  # Keep 5 backup files
            )
            file_handler.setLevel(logging.DEBUG)  # File logs more details
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # Prevent propagation to root logger
        logger.propagate = False

        return logger

    @staticmethod
    def set_level(logger, level):
        """Set the logging level for an existing logger."""
        logger.setLevel(level)
        for handler in logger.handlers:
            handler.setLevel(level)

    @staticmethod
    def add_file_handler(logger, filename=None, level=logging.DEBUG, max_bytes=10485760, backup_count=5):
        """Add a file handler to an existing logger."""
        CustomLogger.ensure_log_directory()
        filename = filename or CustomLogger.DEFAULT_LOG_FILE
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler = RotatingFileHandler(
            filename=filename,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def allureLogs(text):
        with allure.step(text):
            pass