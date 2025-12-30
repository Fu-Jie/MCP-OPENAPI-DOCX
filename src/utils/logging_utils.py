"""Logging utility functions.

This module provides logging utilities for structured
logging throughout the application.
"""

import logging
import sys
from pathlib import Path
from typing import Any

import structlog


def setup_logging(
    log_level: str = "INFO",
    log_format: str = "json",
    log_file: str | None = None,
) -> None:
    """Setup structured logging.

    Args:
        log_level: Logging level.
        log_format: Output format ('json' or 'text').
        log_file: Optional log file path.
    """
    # Set log level
    level = getattr(logging, log_level.upper(), logging.INFO)

    # Configure processors
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
    ]

    if log_format == "json":
        processors = shared_processors + [
            structlog.processors.JSONRenderer(),
        ]
    else:
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Setup standard logging
    logging.basicConfig(
        level=level,
        format="%(message)s",
        stream=sys.stdout,
    )

    # Add file handler if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        logging.getLogger().addHandler(file_handler)


def get_logger(name: str = __name__) -> structlog.BoundLogger:
    """Get a structured logger.

    Args:
        name: Logger name.

    Returns:
        Bound logger instance.
    """
    return structlog.get_logger(name)


class LoggerMixin:
    """Mixin class for adding logging capability.

    Classes that inherit from this mixin get a `logger` attribute.
    """

    @property
    def logger(self) -> structlog.BoundLogger:
        """Get logger for this class.

        Returns:
            Logger instance.
        """
        return get_logger(self.__class__.__name__)


def log_function_call(logger: structlog.BoundLogger):
    """Decorator for logging function calls.

    Args:
        logger: Logger to use.

    Returns:
        Decorator function.
    """
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            logger.info(
                "Function called",
                function=func.__name__,
                args_count=len(args),
                kwargs_keys=list(kwargs.keys()),
            )
            try:
                result = await func(*args, **kwargs)
                logger.info(
                    "Function completed",
                    function=func.__name__,
                )
                return result
            except Exception as e:
                logger.error(
                    "Function failed",
                    function=func.__name__,
                    error=str(e),
                )
                raise

        def sync_wrapper(*args, **kwargs):
            logger.info(
                "Function called",
                function=func.__name__,
                args_count=len(args),
                kwargs_keys=list(kwargs.keys()),
            )
            try:
                result = func(*args, **kwargs)
                logger.info(
                    "Function completed",
                    function=func.__name__,
                )
                return result
            except Exception as e:
                logger.error(
                    "Function failed",
                    function=func.__name__,
                    error=str(e),
                )
                raise

        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


def log_request(
    logger: structlog.BoundLogger,
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    **extra: Any,
) -> None:
    """Log an HTTP request.

    Args:
        logger: Logger to use.
        method: HTTP method.
        path: Request path.
        status_code: Response status code.
        duration_ms: Request duration in milliseconds.
        **extra: Additional fields to log.
    """
    log_data = {
        "method": method,
        "path": path,
        "status_code": status_code,
        "duration_ms": round(duration_ms, 2),
        **extra,
    }

    if status_code >= 500:
        logger.error("HTTP Request", **log_data)
    elif status_code >= 400:
        logger.warning("HTTP Request", **log_data)
    else:
        logger.info("HTTP Request", **log_data)


def log_database_query(
    logger: structlog.BoundLogger,
    query: str,
    duration_ms: float,
    rows_affected: int = 0,
) -> None:
    """Log a database query.

    Args:
        logger: Logger to use.
        query: SQL query (truncated).
        duration_ms: Query duration in milliseconds.
        rows_affected: Number of rows affected.
    """
    # Truncate long queries
    query_preview = query[:200] + "..." if len(query) > 200 else query

    logger.debug(
        "Database Query",
        query=query_preview,
        duration_ms=round(duration_ms, 2),
        rows_affected=rows_affected,
    )
