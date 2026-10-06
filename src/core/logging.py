"""Logging setup."""

import logging

from core.config import Settings


def configure_logging(settings: Settings) -> None:
    """Configure the root logger from settings."""
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
