"""Core package for application configuration and utilities."""

from src.core.config import Settings, get_settings
from src.core.constants import (
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    SUPPORTED_FORMATS,
)
from src.core.enums import (
    DocumentFormat,
    DocumentStatus,
    ExportFormat,
    RevisionAction,
    UserRole,
)
from src.core.exceptions import (
    BaseDocxException,
    DocumentNotFoundError,
    InvalidDocumentError,
    PermissionDeniedError,
    ValidationError,
)

__all__ = [
    "Settings",
    "get_settings",
    "DEFAULT_PAGE_SIZE",
    "MAX_PAGE_SIZE",
    "SUPPORTED_FORMATS",
    "DocumentFormat",
    "DocumentStatus",
    "ExportFormat",
    "RevisionAction",
    "UserRole",
    "BaseDocxException",
    "DocumentNotFoundError",
    "InvalidDocumentError",
    "PermissionDeniedError",
    "ValidationError",
]
