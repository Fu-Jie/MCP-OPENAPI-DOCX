"""Text service for text editing operations.

This module provides the TextService class for paragraph
and text formatting operations.
"""

from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.document_handler import DocumentHandler
from src.handlers.text_handler import TextHandler
from src.core.exceptions import DocumentNotFoundError, DocumentProcessingError


class TextService:
    """Service class for text operations.

    Attributes:
        db: Database session.
        document_handler: Handler for document operations.
        text_handler: Handler for text operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the text service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.document_handler = DocumentHandler()
        self.text_handler = TextHandler()

    async def add_paragraph(
        self,
        document_path: str,
        text: str,
        style: str | None = None,
        position: int | None = None,
    ) -> dict[str, Any]:
        """Add a paragraph to the document.

        Args:
            document_path: Path to the document.
            text: Paragraph text.
            style: Optional paragraph style.
            position: Optional position to insert.

        Returns:
            Result with paragraph details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            para = self.text_handler.add_paragraph(doc, text, style)
            self.document_handler.save_document(doc, document_path)
            return {
                "success": True,
                "text": text,
                "style": style,
            }
        except Exception as e:
            raise DocumentProcessingError(f"Failed to add paragraph: {str(e)}")

    async def update_paragraph(
        self,
        document_path: str,
        paragraph_index: int,
        text: str | None = None,
        style: str | None = None,
    ) -> dict[str, Any]:
        """Update a paragraph in the document.

        Args:
            document_path: Path to the document.
            paragraph_index: Index of paragraph to update.
            text: Optional new text.
            style: Optional new style.

        Returns:
            Result with updated paragraph details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            result = self.text_handler.update_paragraph(
                doc, paragraph_index, text, style
            )
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "updated": result}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to update paragraph: {str(e)}")

    async def delete_paragraph(
        self,
        document_path: str,
        paragraph_index: int,
    ) -> dict[str, Any]:
        """Delete a paragraph from the document.

        Args:
            document_path: Path to the document.
            paragraph_index: Index of paragraph to delete.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.text_handler.delete_paragraph(doc, paragraph_index)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "deleted_index": paragraph_index}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to delete paragraph: {str(e)}")

    async def get_paragraphs(
        self,
        document_path: str,
        start: int | None = None,
        end: int | None = None,
    ) -> list[dict[str, Any]]:
        """Get paragraphs from the document.

        Args:
            document_path: Path to the document.
            start: Optional start index.
            end: Optional end index.

        Returns:
            List of paragraph data.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.text_handler.get_paragraphs(doc, start, end)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to get paragraphs: {str(e)}")

    async def format_text(
        self,
        document_path: str,
        paragraph_index: int,
        run_index: int | None = None,
        bold: bool | None = None,
        italic: bool | None = None,
        underline: bool | None = None,
        font_name: str | None = None,
        font_size: int | None = None,
        color: str | None = None,
    ) -> dict[str, Any]:
        """Apply formatting to text.

        Args:
            document_path: Path to the document.
            paragraph_index: Index of paragraph.
            run_index: Optional run index within paragraph.
            bold: Optional bold setting.
            italic: Optional italic setting.
            underline: Optional underline setting.
            font_name: Optional font name.
            font_size: Optional font size in points.
            color: Optional text color (hex).

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.text_handler.format_text(
                doc,
                paragraph_index,
                run_index,
                bold=bold,
                italic=italic,
                underline=underline,
                font_name=font_name,
                font_size=font_size,
                color=color,
            )
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "paragraph_index": paragraph_index}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to format text: {str(e)}")
