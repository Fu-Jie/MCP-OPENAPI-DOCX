"""File utility functions.

This module provides utility functions for file operations
including reading, writing, and file management.
"""

import hashlib
import os
import shutil
import tempfile
from pathlib import Path


class FileUtils:
    """Utility class for file operations.

    Provides static methods for common file operations.
    """

    @staticmethod
    def ensure_directory(path: str) -> None:
        """Ensure a directory exists.

        Args:
            path: Directory path.
        """
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def get_file_extension(filename: str) -> str:
        """Get file extension.

        Args:
            filename: File name or path.

        Returns:
            File extension including dot (e.g., '.docx').
        """
        return os.path.splitext(filename)[1].lower()

    @staticmethod
    def get_file_size(path: str) -> int:
        """Get file size in bytes.

        Args:
            path: File path.

        Returns:
            File size in bytes.
        """
        return os.path.getsize(path)

    @staticmethod
    def file_exists(path: str) -> bool:
        """Check if file exists.

        Args:
            path: File path.

        Returns:
            True if file exists.
        """
        return os.path.isfile(path)

    @staticmethod
    def delete_file(path: str) -> bool:
        """Delete a file.

        Args:
            path: File path.

        Returns:
            True if deleted successfully.
        """
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    @staticmethod
    def copy_file(src: str, dest: str) -> str:
        """Copy a file.

        Args:
            src: Source path.
            dest: Destination path.

        Returns:
            Destination path.
        """
        return shutil.copy2(src, dest)

    @staticmethod
    def move_file(src: str, dest: str) -> str:
        """Move a file.

        Args:
            src: Source path.
            dest: Destination path.

        Returns:
            Destination path.
        """
        return shutil.move(src, dest)

    @staticmethod
    def read_binary(path: str) -> bytes:
        """Read file as binary.

        Args:
            path: File path.

        Returns:
            File content as bytes.
        """
        with open(path, "rb") as f:
            return f.read()

    @staticmethod
    def write_binary(path: str, data: bytes) -> None:
        """Write binary data to file.

        Args:
            path: File path.
            data: Binary data.
        """
        with open(path, "wb") as f:
            f.write(data)

    @staticmethod
    def read_text(path: str, encoding: str = "utf-8") -> str:
        """Read file as text.

        Args:
            path: File path.
            encoding: Text encoding.

        Returns:
            File content as string.
        """
        with open(path, encoding=encoding) as f:
            return f.read()

    @staticmethod
    def write_text(path: str, content: str, encoding: str = "utf-8") -> None:
        """Write text to file.

        Args:
            path: File path.
            content: Text content.
            encoding: Text encoding.
        """
        with open(path, "w", encoding=encoding) as f:
            f.write(content)

    @staticmethod
    def get_checksum(path: str, algorithm: str = "sha256") -> str:
        """Calculate file checksum.

        Args:
            path: File path.
            algorithm: Hash algorithm.

        Returns:
            Checksum string.
        """
        hash_func = getattr(hashlib, algorithm)()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    @staticmethod
    def create_temp_file(
        suffix: str = "",
        prefix: str = "tmp",
        content: bytes | None = None,
    ) -> str:
        """Create a temporary file.

        Args:
            suffix: File suffix.
            prefix: File prefix.
            content: Optional initial content.

        Returns:
            Temporary file path.
        """
        fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
        if content:
            os.write(fd, content)
        os.close(fd)
        return path

    @staticmethod
    def create_temp_directory(
        prefix: str = "tmp",
    ) -> str:
        """Create a temporary directory.

        Args:
            prefix: Directory prefix.

        Returns:
            Temporary directory path.
        """
        return tempfile.mkdtemp(prefix=prefix)

    @staticmethod
    def list_files(
        directory: str,
        pattern: str = "*",
        recursive: bool = False,
    ) -> list[str]:
        """List files in directory.

        Args:
            directory: Directory path.
            pattern: Glob pattern.
            recursive: Search recursively.

        Returns:
            List of file paths.
        """
        path = Path(directory)
        if recursive:
            return [str(p) for p in path.rglob(pattern) if p.is_file()]
        return [str(p) for p in path.glob(pattern) if p.is_file()]

    @staticmethod
    def get_mime_type(path: str) -> str:
        """Get file MIME type.

        Args:
            path: File path.

        Returns:
            MIME type string.
        """
        import mimetypes

        mime_type, _ = mimetypes.guess_type(path)
        return mime_type or "application/octet-stream"

    @staticmethod
    def safe_filename(filename: str) -> str:
        """Sanitize filename for safe storage.

        Args:
            filename: Original filename.

        Returns:
            Sanitized filename.
        """
        import re

        # Remove path separators and dangerous characters
        safe = re.sub(r'[<>:"/\\|?*]', "", filename)
        # Remove leading/trailing spaces and dots
        safe = safe.strip(" .")
        return safe or "unnamed"
