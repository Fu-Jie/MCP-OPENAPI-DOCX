"""Compression utility functions.

This module provides compression utilities for working with
compressed files and data.
"""

import gzip
import io
import zipfile
from typing import Any


class CompressionUtils:
    """Utility class for compression operations.

    Provides static methods for compressing and decompressing data.
    """

    @staticmethod
    def gzip_compress(data: bytes, level: int = 9) -> bytes:
        """Compress data using gzip.

        Args:
            data: Data to compress.
            level: Compression level (0-9).

        Returns:
            Compressed data.
        """
        return gzip.compress(data, compresslevel=level)

    @staticmethod
    def gzip_decompress(data: bytes) -> bytes:
        """Decompress gzip data.

        Args:
            data: Compressed data.

        Returns:
            Decompressed data.
        """
        return gzip.decompress(data)

    @staticmethod
    def create_zip(
        files: dict[str, bytes],
        compression: int = zipfile.ZIP_DEFLATED,
    ) -> bytes:
        """Create a ZIP archive.

        Args:
            files: Dictionary of filename to content.
            compression: Compression method.

        Returns:
            ZIP file as bytes.
        """
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", compression=compression) as zf:
            for filename, content in files.items():
                zf.writestr(filename, content)
        return buffer.getvalue()

    @staticmethod
    def extract_zip(data: bytes) -> dict[str, bytes]:
        """Extract files from ZIP archive.

        Args:
            data: ZIP file bytes.

        Returns:
            Dictionary of filename to content.
        """
        buffer = io.BytesIO(data)
        files = {}
        with zipfile.ZipFile(buffer, "r") as zf:
            for name in zf.namelist():
                files[name] = zf.read(name)
        return files

    @staticmethod
    def list_zip_contents(data: bytes) -> list[dict[str, Any]]:
        """List ZIP archive contents.

        Args:
            data: ZIP file bytes.

        Returns:
            List of file info dictionaries.
        """
        buffer = io.BytesIO(data)
        contents = []
        with zipfile.ZipFile(buffer, "r") as zf:
            for info in zf.infolist():
                contents.append(
                    {
                        "filename": info.filename,
                        "file_size": info.file_size,
                        "compress_size": info.compress_size,
                        "is_dir": info.is_dir(),
                    }
                )
        return contents

    @staticmethod
    def add_to_zip(zip_data: bytes, filename: str, content: bytes) -> bytes:
        """Add a file to existing ZIP.

        Args:
            zip_data: Existing ZIP bytes.
            filename: Name for new file.
            content: File content.

        Returns:
            Updated ZIP bytes.
        """
        buffer = io.BytesIO(zip_data)
        with zipfile.ZipFile(buffer, "a") as zf:
            zf.writestr(filename, content)
        return buffer.getvalue()

    @staticmethod
    def is_valid_zip(data: bytes) -> bool:
        """Check if data is valid ZIP.

        Args:
            data: Data to check.

        Returns:
            True if valid ZIP.
        """
        try:
            buffer = io.BytesIO(data)
            with zipfile.ZipFile(buffer, "r") as zf:
                return zf.testzip() is None
        except Exception:
            return False

    @staticmethod
    def get_compression_ratio(original: bytes, compressed: bytes) -> float:
        """Calculate compression ratio.

        Args:
            original: Original data.
            compressed: Compressed data.

        Returns:
            Compression ratio (0-1).
        """
        if len(original) == 0:
            return 0.0
        return 1 - (len(compressed) / len(original))
