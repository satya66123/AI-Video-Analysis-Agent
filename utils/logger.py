"""
utils/logger.py
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.settings import LOG_DIR


class Logger:

    _initialized = False

    @classmethod
    def initialize(cls):

        if cls._initialized:
            return

        LOG_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        formatter = logging.Formatter(
            "[%(asctime)s] "
            "[%(levelname)s] "
            "%(name)s : %(message)s"
        )

        file_handler = RotatingFileHandler(
            Path(LOG_DIR) / "application.log",
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )

        file_handler.setFormatter(
            formatter
        )

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(
            formatter
        )

        logging.basicConfig(
            level=logging.INFO,
            handlers=[
                file_handler,
                console_handler,
            ],
        )

        cls._initialized = True

    @classmethod
    def get_logger(
        cls,
        name: str,
    ):

        cls.initialize()

        return logging.getLogger(name)