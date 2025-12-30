"""Application constants and fixed values.

This module contains all constant values used throughout the application.
"""

from typing import Final

# =============================================================================
# Pagination Constants
# =============================================================================
DEFAULT_PAGE_SIZE: Final[int] = 20
MAX_PAGE_SIZE: Final[int] = 100
MIN_PAGE_SIZE: Final[int] = 1

# =============================================================================
# Document Constants
# =============================================================================
DOCX_MIME_TYPE: Final[str] = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)
DOC_MIME_TYPE: Final[str] = "application/msword"
PDF_MIME_TYPE: Final[str] = "application/pdf"
HTML_MIME_TYPE: Final[str] = "text/html"
MARKDOWN_MIME_TYPE: Final[str] = "text/markdown"

SUPPORTED_FORMATS: Final[dict[str, str]] = {
    ".docx": DOCX_MIME_TYPE,
    ".doc": DOC_MIME_TYPE,
    ".pdf": PDF_MIME_TYPE,
    ".html": HTML_MIME_TYPE,
    ".md": MARKDOWN_MIME_TYPE,
}

# =============================================================================
# Style Constants
# =============================================================================
DEFAULT_FONT_NAME: Final[str] = "Calibri"
DEFAULT_FONT_SIZE: Final[int] = 11
DEFAULT_HEADING_FONT: Final[str] = "Calibri Light"
DEFAULT_LINE_SPACING: Final[float] = 1.15

# Font size ranges (in points)
MIN_FONT_SIZE: Final[int] = 6
MAX_FONT_SIZE: Final[int] = 144

# =============================================================================
# Color Constants
# =============================================================================
COLOR_BLACK: Final[str] = "000000"
COLOR_WHITE: Final[str] = "FFFFFF"
COLOR_RED: Final[str] = "FF0000"
COLOR_GREEN: Final[str] = "00FF00"
COLOR_BLUE: Final[str] = "0000FF"
COLOR_YELLOW: Final[str] = "FFFF00"
COLOR_GRAY: Final[str] = "808080"

# =============================================================================
# Layout Constants
# =============================================================================
# Default page margins in inches
DEFAULT_MARGIN_TOP: Final[float] = 1.0
DEFAULT_MARGIN_BOTTOM: Final[float] = 1.0
DEFAULT_MARGIN_LEFT: Final[float] = 1.0
DEFAULT_MARGIN_RIGHT: Final[float] = 1.0

# Page sizes in inches (width x height)
PAGE_SIZE_LETTER: Final[tuple[float, float]] = (8.5, 11)
PAGE_SIZE_A4: Final[tuple[float, float]] = (8.27, 11.69)
PAGE_SIZE_LEGAL: Final[tuple[float, float]] = (8.5, 14)
PAGE_SIZE_A3: Final[tuple[float, float]] = (11.69, 16.54)

# =============================================================================
# Table Constants
# =============================================================================
MAX_TABLE_COLUMNS: Final[int] = 63
MAX_TABLE_ROWS: Final[int] = 32767
DEFAULT_CELL_WIDTH: Final[float] = 1.5  # inches

# =============================================================================
# Image Constants
# =============================================================================
SUPPORTED_IMAGE_FORMATS: Final[list[str]] = [
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"
]
MAX_IMAGE_DIMENSION: Final[int] = 10000  # pixels
DEFAULT_IMAGE_DPI: Final[int] = 96

# =============================================================================
# API Constants
# =============================================================================
API_V1_PREFIX: Final[str] = "/api/v1"
OPENAPI_TITLE: Final[str] = "MCP-OPENAPI-DOCX API"
OPENAPI_DESCRIPTION: Final[str] = """
Enterprise-grade document editing and management server supporting 
MCP (Model Context Protocol) and OpenAPI protocols for DOCX documents.

## Features

* **Document Management**: Create, read, update, delete DOCX documents
* **Text Editing**: Full text manipulation with formatting
* **Table Operations**: Create and modify tables with advanced features
* **Media Handling**: Insert and manage images and shapes
* **Style Management**: Apply and customize document styles
* **Layout Control**: Page setup, margins, headers, footers
* **TOC & Navigation**: Table of contents, bookmarks, hyperlinks
* **Comments & Revisions**: Track changes and add comments
* **Export**: Convert to PDF, HTML, Markdown
* **MCP Integration**: Full MCP protocol support for AI assistants

## Authentication

Use JWT tokens for authentication. Include the token in the Authorization header:
```
Authorization: Bearer <token>
```
"""
OPENAPI_VERSION: Final[str] = "1.0.0"

# =============================================================================
# MCP Constants
# =============================================================================
MCP_PROTOCOL_VERSION: Final[str] = "2024-11-05"
MCP_SERVER_CAPABILITIES: Final[list[str]] = [
    "tools",
    "resources",
    "prompts",
    "logging",
]

# =============================================================================
# Error Messages
# =============================================================================
ERROR_DOCUMENT_NOT_FOUND: Final[str] = "Document not found"
ERROR_INVALID_DOCUMENT: Final[str] = "Invalid document format"
ERROR_PERMISSION_DENIED: Final[str] = "Permission denied"
ERROR_VALIDATION_FAILED: Final[str] = "Validation failed"
ERROR_FILE_TOO_LARGE: Final[str] = "File size exceeds maximum limit"
ERROR_UNSUPPORTED_FORMAT: Final[str] = "Unsupported file format"
ERROR_INTERNAL_SERVER: Final[str] = "Internal server error"
ERROR_RATE_LIMIT_EXCEEDED: Final[str] = "Rate limit exceeded"
ERROR_AUTHENTICATION_REQUIRED: Final[str] = "Authentication required"
ERROR_INVALID_TOKEN: Final[str] = "Invalid or expired token"

# =============================================================================
# Cache Keys
# =============================================================================
CACHE_PREFIX: Final[str] = "docx:"
CACHE_DOCUMENT_KEY: Final[str] = "docx:document:{document_id}"
CACHE_USER_KEY: Final[str] = "docx:user:{user_id}"
CACHE_TEMPLATE_KEY: Final[str] = "docx:template:{template_id}"

# =============================================================================
# Database Constants
# =============================================================================
DB_NAMING_CONVENTION: Final[dict[str, str]] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
