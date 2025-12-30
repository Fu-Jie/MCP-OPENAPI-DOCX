"""Layout service for page layout operations.

This module provides the LayoutService class for managing
page settings, sections, and headers/footers.
"""

from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.document_handler import DocumentHandler
from src.handlers.layout_handler import LayoutHandler
from src.core.exceptions import DocumentProcessingError


class LayoutService:
    """Service class for layout operations.

    Attributes:
        db: Database session.
        document_handler: Handler for document operations.
        layout_handler: Handler for layout operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the layout service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.document_handler = DocumentHandler()
        self.layout_handler = LayoutHandler()

    async def get_page_settings(
        self,
        document_path: str,
        section_index: int = 0,
    ) -> dict[str, Any]:
        """Get page settings for a section.

        Args:
            document_path: Path to the document.
            section_index: Section index (default 0).

        Returns:
            Page settings dictionary.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.layout_handler.get_page_settings(doc, section_index)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to get settings: {str(e)}")

    async def set_page_size(
        self,
        document_path: str,
        width: float,
        height: float,
        section_index: int = 0,
    ) -> dict[str, Any]:
        """Set page size.

        Args:
            document_path: Path to the document.
            width: Page width in inches.
            height: Page height in inches.
            section_index: Section index.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.layout_handler.set_page_size(doc, width, height, section_index)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "width": width, "height": height}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to set page size: {str(e)}")

    async def set_margins(
        self,
        document_path: str,
        top: float | None = None,
        bottom: float | None = None,
        left: float | None = None,
        right: float | None = None,
        section_index: int = 0,
    ) -> dict[str, Any]:
        """Set page margins.

        Args:
            document_path: Path to the document.
            top: Top margin in inches.
            bottom: Bottom margin in inches.
            left: Left margin in inches.
            right: Right margin in inches.
            section_index: Section index.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.layout_handler.set_margins(
                doc, top, bottom, left, right, section_index
            )
            self.document_handler.save_document(doc, document_path)
            return {"success": True}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to set margins: {str(e)}")

    async def set_orientation(
        self,
        document_path: str,
        orientation: str,
        section_index: int = 0,
    ) -> dict[str, Any]:
        """Set page orientation.

        Args:
            document_path: Path to the document.
            orientation: 'portrait' or 'landscape'.
            section_index: Section index.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.layout_handler.set_orientation(doc, orientation, section_index)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "orientation": orientation}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to set orientation: {str(e)}")

    async def add_section(
        self,
        document_path: str,
        start_type: str = "next_page",
    ) -> dict[str, Any]:
        """Add a new section.

        Args:
            document_path: Path to the document.
            start_type: Section start type.

        Returns:
            Result with section details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.layout_handler.add_section(doc, start_type)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "start_type": start_type}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to add section: {str(e)}")

    async def get_sections(
        self,
        document_path: str,
    ) -> list[dict[str, Any]]:
        """Get all sections.

        Args:
            document_path: Path to the document.

        Returns:
            List of section information.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.layout_handler.get_sections(doc)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to get sections: {str(e)}")

    async def set_header(
        self,
        document_path: str,
        text: str,
        section_index: int = 0,
    ) -> dict[str, Any]:
        """Set header text.

        Args:
            document_path: Path to the document.
            text: Header text.
            section_index: Section index.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.layout_handler.set_header(doc, text, section_index)
            self.document_handler.save_document(doc, document_path)
            return {"success": True}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to set header: {str(e)}")

    async def set_footer(
        self,
        document_path: str,
        text: str,
        section_index: int = 0,
    ) -> dict[str, Any]:
        """Set footer text.

        Args:
            document_path: Path to the document.
            text: Footer text.
            section_index: Section index.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.layout_handler.set_footer(doc, text, section_index)
            self.document_handler.save_document(doc, document_path)
            return {"success": True}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to set footer: {str(e)}")

    async def add_page_numbers(
        self,
        document_path: str,
        position: str = "footer",
        alignment: str = "center",
    ) -> dict[str, Any]:
        """Add page numbers.

        Args:
            document_path: Path to the document.
            position: 'header' or 'footer'.
            alignment: 'left', 'center', or 'right'.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.layout_handler.add_page_numbers(doc, position, alignment)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "position": position, "alignment": alignment}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to add page numbers: {str(e)}")
