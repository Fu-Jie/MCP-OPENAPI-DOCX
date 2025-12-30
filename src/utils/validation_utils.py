"""Validation utility functions.

This module provides validation utilities for validating
various types of data including documents, files, and inputs.
"""

import os
import re
from typing import Any


class ValidationUtils:
    """Utility class for validation operations.

    Provides static methods for common validation tasks.
    """

    # Allowed document extensions
    ALLOWED_EXTENSIONS = {".docx", ".doc"}
    ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"}

    # Maximum file sizes (in bytes)
    MAX_DOCUMENT_SIZE = 100 * 1024 * 1024  # 100MB
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB

    @staticmethod
    def is_valid_document_extension(filename: str) -> bool:
        """Check if file has valid document extension.

        Args:
            filename: File name or path.

        Returns:
            True if extension is valid.
        """
        ext = os.path.splitext(filename)[1].lower()
        return ext in ValidationUtils.ALLOWED_EXTENSIONS

    @staticmethod
    def is_valid_image_extension(filename: str) -> bool:
        """Check if file has valid image extension.

        Args:
            filename: File name or path.

        Returns:
            True if extension is valid.
        """
        ext = os.path.splitext(filename)[1].lower()
        return ext in ValidationUtils.ALLOWED_IMAGE_EXTENSIONS

    @staticmethod
    def is_valid_file_size(
        size: int,
        max_size: int | None = None,
    ) -> bool:
        """Check if file size is valid.

        Args:
            size: File size in bytes.
            max_size: Optional maximum size.

        Returns:
            True if size is valid.
        """
        max_allowed = max_size or ValidationUtils.MAX_DOCUMENT_SIZE
        return 0 < size <= max_allowed

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format.

        Args:
            email: Email address.

        Returns:
            True if email is valid.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def is_valid_uuid(value: str) -> bool:
        """Validate UUID format.

        Args:
            value: UUID string.

        Returns:
            True if valid UUID.
        """
        pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        return bool(re.match(pattern, value.lower()))

    @staticmethod
    def is_valid_color(color: str) -> bool:
        """Validate color format (hex).

        Args:
            color: Color string.

        Returns:
            True if valid hex color.
        """
        pattern = r"^#?([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})$"
        return bool(re.match(pattern, color))

    @staticmethod
    def sanitize_string(
        value: str,
        max_length: int | None = None,
        strip: bool = True,
    ) -> str:
        """Sanitize a string value.

        Args:
            value: Input string.
            max_length: Optional maximum length.
            strip: Strip whitespace.

        Returns:
            Sanitized string.
        """
        if strip:
            value = value.strip()
        if max_length:
            value = value[:max_length]
        return value

    @staticmethod
    def validate_pagination(
        skip: int,
        limit: int,
        max_limit: int = 100,
    ) -> tuple[int, int]:
        """Validate pagination parameters.

        Args:
            skip: Number to skip.
            limit: Maximum to return.
            max_limit: Maximum allowed limit.

        Returns:
            Validated (skip, limit) tuple.
        """
        skip = max(0, skip)
        limit = max(1, min(limit, max_limit))
        return skip, limit

    @staticmethod
    def is_valid_paragraph_index(index: int, max_index: int) -> bool:
        """Validate paragraph index.

        Args:
            index: Paragraph index.
            max_index: Maximum valid index.

        Returns:
            True if valid index.
        """
        return 0 <= index <= max_index

    @staticmethod
    def is_valid_table_coords(
        row: int,
        col: int,
        max_rows: int,
        max_cols: int,
    ) -> bool:
        """Validate table coordinates.

        Args:
            row: Row index.
            col: Column index.
            max_rows: Maximum rows.
            max_cols: Maximum columns.

        Returns:
            True if coordinates are valid.
        """
        return 0 <= row < max_rows and 0 <= col < max_cols

    @staticmethod
    def validate_font_size(size: int) -> bool:
        """Validate font size.

        Args:
            size: Font size in points.

        Returns:
            True if valid size.
        """
        return 1 <= size <= 999

    @staticmethod
    def validate_margin(margin: float) -> bool:
        """Validate margin value.

        Args:
            margin: Margin in inches.

        Returns:
            True if valid margin.
        """
        return 0 <= margin <= 10

    @staticmethod
    def validate_required_fields(
        data: dict[str, Any],
        required: list[str],
    ) -> list[str]:
        """Validate required fields are present.

        Args:
            data: Data dictionary.
            required: List of required field names.

        Returns:
            List of missing fields.
        """
        missing = []
        for field in required:
            if field not in data or data[field] is None:
                missing.append(field)
        return missing

    @staticmethod
    def is_docx_file(content: bytes) -> bool:
        """Check if content is a valid DOCX file.

        Args:
            content: File content bytes.

        Returns:
            True if valid DOCX.
        """
        # DOCX files are ZIP archives starting with PK
        return content[:2] == b"PK"
