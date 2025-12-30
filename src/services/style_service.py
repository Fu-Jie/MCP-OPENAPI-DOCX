"""Style service for document styling operations.

This module provides the StyleService class for managing
document styles and formatting.
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import DocumentProcessingError
from src.handlers.document_handler import DocumentHandler
from src.handlers.style_handler import StyleHandler


class StyleService:
    """Service class for style operations.

    Attributes:
        db: Database session.
        document_handler: Handler for document operations.
        style_handler: Handler for style operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the style service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.document_handler = DocumentHandler()
        self.style_handler = StyleHandler()

    async def get_styles(
        self,
        document_path: str,
        style_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get all styles in the document.

        Args:
            document_path: Path to the document.
            style_type: Optional filter by type (paragraph, character, table).

        Returns:
            List of style information.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.style_handler.get_styles(doc, style_type)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to get styles: {str(e)}")

    async def apply_style(
        self,
        document_path: str,
        style_name: str,
        paragraph_index: int | None = None,
        run_index: int | None = None,
    ) -> dict[str, Any]:
        """Apply a style to content.

        Args:
            document_path: Path to the document.
            style_name: Name of the style to apply.
            paragraph_index: Optional paragraph index.
            run_index: Optional run index.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.style_handler.apply_style(doc, style_name, paragraph_index, run_index)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "style": style_name}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to apply style: {str(e)}")

    async def create_style(
        self,
        document_path: str,
        name: str,
        style_type: str = "paragraph",
        base_style: str | None = None,
        font_name: str | None = None,
        font_size: int | None = None,
        bold: bool | None = None,
        italic: bool | None = None,
        color: str | None = None,
    ) -> dict[str, Any]:
        """Create a new style.

        Args:
            document_path: Path to the document.
            name: Style name.
            style_type: Type of style (paragraph, character, table).
            base_style: Optional base style to inherit from.
            font_name: Optional font name.
            font_size: Optional font size.
            bold: Optional bold setting.
            italic: Optional italic setting.
            color: Optional text color.

        Returns:
            Result with style details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.style_handler.create_style(
                doc,
                name,
                style_type,
                base_style,
                font_name,
                font_size,
                bold,
                italic,
                color,
            )
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "name": name, "type": style_type}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to create style: {str(e)}")

    async def modify_style(
        self,
        document_path: str,
        name: str,
        font_name: str | None = None,
        font_size: int | None = None,
        bold: bool | None = None,
        italic: bool | None = None,
        color: str | None = None,
    ) -> dict[str, Any]:
        """Modify an existing style.

        Args:
            document_path: Path to the document.
            name: Style name.
            font_name: Optional new font name.
            font_size: Optional new font size.
            bold: Optional new bold setting.
            italic: Optional new italic setting.
            color: Optional new text color.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.style_handler.modify_style(
                doc, name, font_name, font_size, bold, italic, color
            )
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "name": name}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to modify style: {str(e)}")

    async def delete_style(
        self,
        document_path: str,
        name: str,
    ) -> dict[str, Any]:
        """Delete a style.

        Args:
            document_path: Path to the document.
            name: Style name.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.style_handler.delete_style(doc, name)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "deleted": name}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to delete style: {str(e)}")
