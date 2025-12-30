"""TOC service for table of contents operations.

This module provides the TocService class for managing
table of contents, bookmarks, and hyperlinks.
"""

from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.document_handler import DocumentHandler
from src.handlers.toc_handler import TocHandler
from src.core.exceptions import DocumentProcessingError


class TocService:
    """Service class for TOC operations.

    Attributes:
        db: Database session.
        document_handler: Handler for document operations.
        toc_handler: Handler for TOC operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the TOC service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.document_handler = DocumentHandler()
        self.toc_handler = TocHandler()

    async def generate_toc(
        self,
        document_path: str,
        heading_levels: int = 3,
        title: str = "Table of Contents",
    ) -> dict[str, Any]:
        """Generate table of contents.

        Args:
            document_path: Path to the document.
            heading_levels: Number of heading levels to include.
            title: TOC title.

        Returns:
            Result with TOC details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.toc_handler.generate_toc(doc, heading_levels, title)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "levels": heading_levels}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to generate TOC: {str(e)}")

    async def update_toc(
        self,
        document_path: str,
    ) -> dict[str, Any]:
        """Update table of contents.

        Args:
            document_path: Path to the document.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.toc_handler.update_toc(doc)
            self.document_handler.save_document(doc, document_path)
            return {"success": True}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to update TOC: {str(e)}")

    async def add_bookmark(
        self,
        document_path: str,
        name: str,
        paragraph_index: int,
    ) -> dict[str, Any]:
        """Add a bookmark.

        Args:
            document_path: Path to the document.
            name: Bookmark name.
            paragraph_index: Paragraph index.

        Returns:
            Result with bookmark details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.toc_handler.add_bookmark(doc, name, paragraph_index)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "name": name}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to add bookmark: {str(e)}")

    async def get_bookmarks(
        self,
        document_path: str,
    ) -> list[dict[str, Any]]:
        """Get all bookmarks.

        Args:
            document_path: Path to the document.

        Returns:
            List of bookmarks.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.toc_handler.get_bookmarks(doc)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to get bookmarks: {str(e)}")

    async def delete_bookmark(
        self,
        document_path: str,
        name: str,
    ) -> dict[str, Any]:
        """Delete a bookmark.

        Args:
            document_path: Path to the document.
            name: Bookmark name.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.toc_handler.delete_bookmark(doc, name)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "deleted": name}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to delete bookmark: {str(e)}")

    async def add_hyperlink(
        self,
        document_path: str,
        url: str,
        text: str,
        paragraph_index: int | None = None,
    ) -> dict[str, Any]:
        """Add a hyperlink.

        Args:
            document_path: Path to the document.
            url: Link URL.
            text: Link text.
            paragraph_index: Optional paragraph index.

        Returns:
            Result with link details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.toc_handler.add_hyperlink(doc, url, text, paragraph_index)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "url": url, "text": text}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to add hyperlink: {str(e)}")

    async def get_hyperlinks(
        self,
        document_path: str,
    ) -> list[dict[str, Any]]:
        """Get all hyperlinks.

        Args:
            document_path: Path to the document.

        Returns:
            List of hyperlinks.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.toc_handler.get_hyperlinks(doc)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to get hyperlinks: {str(e)}")

    async def add_internal_link(
        self,
        document_path: str,
        bookmark_name: str,
        text: str,
        paragraph_index: int | None = None,
    ) -> dict[str, Any]:
        """Add an internal link to a bookmark.

        Args:
            document_path: Path to the document.
            bookmark_name: Target bookmark name.
            text: Link text.
            paragraph_index: Optional paragraph index.

        Returns:
            Result with link details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.toc_handler.add_internal_link(doc, bookmark_name, text, paragraph_index)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "bookmark": bookmark_name, "text": text}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to add internal link: {str(e)}")
