"""
Centralized logging configuration using structlog.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

import structlog
from structlog.typing import FilteringBoundLogger

from src.config.settings import Settings, get_settings


def configure_logging(
    settings: Optional[Settings] = None,
    log_file: Optional[str] = None
) -> None:
    """
    Configure structured logging for the application.

    Args:
        settings: Application settings (auto-loaded if not provided)
        log_file: Optional log file path (overrides settings)
    """
    settings = settings or get_settings()
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Create processors based on format
    if settings.log_format == "json":
        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ]
    else:
        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer(colors=True)
        ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard logging
    handlers = [logging.StreamHandler(sys.stdout)]

    # Add file handler if log file specified
    log_path = log_file or settings.log_file
    if log_path:
        log_dir = Path(log_path).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_path))

    logging.basicConfig(
        format="%(message)s",
        level=log_level,
        handlers=handlers,
        force=True
    )

    # Silence noisy loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def get_logger(name: str = None) -> FilteringBoundLogger:
    """
    Get a structured logger instance.

    Args:
        name: Logger name (optional)

    Returns:
        Configured structlog logger
    """
    if name:
        return structlog.get_logger(name)
    return structlog.get_logger()
