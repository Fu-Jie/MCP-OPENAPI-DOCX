"""List service for list operations.

This module provides the ListService class for creating
and managing lists in documents.
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import DocumentProcessingError
from src.handlers.document_handler import DocumentHandler
from src.handlers.list_handler import ListHandler


class ListService:
    """Service class for list operations.

    Attributes:
        db: Database session.
        document_handler: Handler for document operations.
        list_handler: Handler for list operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the list service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.document_handler = DocumentHandler()
        self.list_handler = ListHandler()

    async def create_bulleted_list(
        self,
        document_path: str,
        items: list[str],
        style: str | None = None,
    ) -> dict[str, Any]:
        """Create a bulleted list.

        Args:
            document_path: Path to the document.
            items: List items.
            style: Optional list style.

        Returns:
            Result with list details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.list_handler.create_bulleted_list(doc, items, style)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "type": "bulleted", "items": len(items)}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to create list: {str(e)}")

    async def create_numbered_list(
        self,
        document_path: str,
        items: list[str],
        start: int = 1,
        style: str | None = None,
    ) -> dict[str, Any]:
        """Create a numbered list.

        Args:
            document_path: Path to the document.
            items: List items.
            start: Starting number.
            style: Optional list style.

        Returns:
            Result with list details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.list_handler.create_numbered_list(doc, items, start, style)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "type": "numbered", "items": len(items)}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to create list: {str(e)}")

    async def add_list_item(
        self,
        document_path: str,
        list_paragraph_index: int,
        text: str,
        level: int = 0,
    ) -> dict[str, Any]:
        """Add an item to a list.

        Args:
            document_path: Path to the document.
            list_paragraph_index: Index of list paragraph.
            text: Item text.
            level: Indentation level.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.list_handler.add_list_item(doc, list_paragraph_index, text, level)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "text": text, "level": level}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to add list item: {str(e)}")

    async def update_list_item(
        self,
        document_path: str,
        paragraph_index: int,
        text: str | None = None,
        level: int | None = None,
    ) -> dict[str, Any]:
        """Update a list item.

        Args:
            document_path: Path to the document.
            paragraph_index: Index of the paragraph.
            text: Optional new text.
            level: Optional new level.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.list_handler.update_list_item(doc, paragraph_index, text, level)
            self.document_handler.save_document(doc, document_path)
            return {"success": True}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to update list item: {str(e)}")

    async def remove_list_item(
        self,
        document_path: str,
        paragraph_index: int,
    ) -> dict[str, Any]:
        """Remove a list item.

        Args:
            document_path: Path to the document.
            paragraph_index: Index of the paragraph to remove.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.list_handler.remove_list_item(doc, paragraph_index)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "removed_index": paragraph_index}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to remove list item: {str(e)}")

    async def get_lists(
        self,
        document_path: str,
    ) -> list[dict[str, Any]]:
        """Get all lists in document.

        Args:
            document_path: Path to the document.

        Returns:
            List of lists with their items.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.list_handler.get_lists(doc)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to get lists: {str(e)}")
