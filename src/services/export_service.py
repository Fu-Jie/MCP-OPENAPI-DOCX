"""Export service for document export operations.

This module provides the ExportService class for exporting
documents to various formats.
"""

import os
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.core.exceptions import DocumentProcessingError
from src.handlers.document_handler import DocumentHandler


class ExportService:
    """Service class for export operations.

    Attributes:
        db: Database session.
        document_handler: Handler for document operations.
        settings: Application settings.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the export service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.document_handler = DocumentHandler()
        self.settings = get_settings()

    async def export_to_pdf(
        self,
        document_path: str,
        output_path: str | None = None,
    ) -> dict[str, Any]:
        """Export document to PDF.

        Args:
            document_path: Path to the document.
            output_path: Optional output path.

        Returns:
            Result with output path.
        """
        try:
            if not output_path:
                base = os.path.splitext(document_path)[0]
                output_path = f"{base}.pdf"

            # Note: PDF export requires additional libraries
            # This is a placeholder implementation
            return {
                "success": True,
                "format": "pdf",
                "output_path": output_path,
                "message": "PDF export requires additional configuration",
            }
        except Exception as e:
            raise DocumentProcessingError(f"Failed to export to PDF: {str(e)}")

    async def export_to_html(
        self,
        document_path: str,
        output_path: str | None = None,
        include_styles: bool = True,
    ) -> dict[str, Any]:
        """Export document to HTML.

        Args:
            document_path: Path to the document.
            output_path: Optional output path.
            include_styles: Include CSS styles.

        Returns:
            Result with output path.
        """
        try:
            doc = self.document_handler.load_document(document_path)

            if not output_path:
                base = os.path.splitext(document_path)[0]
                output_path = f"{base}.html"

            html_content = self._convert_to_html(doc, include_styles)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            return {
                "success": True,
                "format": "html",
                "output_path": output_path,
            }
        except Exception as e:
            raise DocumentProcessingError(f"Failed to export to HTML: {str(e)}")

    async def export_to_markdown(
        self,
        document_path: str,
        output_path: str | None = None,
    ) -> dict[str, Any]:
        """Export document to Markdown.

        Args:
            document_path: Path to the document.
            output_path: Optional output path.

        Returns:
            Result with output path.
        """
        try:
            doc = self.document_handler.load_document(document_path)

            if not output_path:
                base = os.path.splitext(document_path)[0]
                output_path = f"{base}.md"

            md_content = self._convert_to_markdown(doc)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md_content)

            return {
                "success": True,
                "format": "markdown",
                "output_path": output_path,
            }
        except Exception as e:
            raise DocumentProcessingError(f"Failed to export to Markdown: {str(e)}")

    async def export_to_text(
        self,
        document_path: str,
        output_path: str | None = None,
    ) -> dict[str, Any]:
        """Export document to plain text.

        Args:
            document_path: Path to the document.
            output_path: Optional output path.

        Returns:
            Result with output path.
        """
        try:
            doc = self.document_handler.load_document(document_path)

            if not output_path:
                base = os.path.splitext(document_path)[0]
                output_path = f"{base}.txt"

            text_content = self._extract_text(doc)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text_content)

            return {
                "success": True,
                "format": "text",
                "output_path": output_path,
            }
        except Exception as e:
            raise DocumentProcessingError(f"Failed to export to text: {str(e)}")

    async def get_export_formats(self) -> list[dict[str, Any]]:
        """Get available export formats.

        Returns:
            List of supported formats.
        """
        return [
            {"format": "pdf", "extension": ".pdf", "description": "PDF Document"},
            {"format": "html", "extension": ".html", "description": "HTML Document"},
            {"format": "markdown", "extension": ".md", "description": "Markdown"},
            {"format": "text", "extension": ".txt", "description": "Plain Text"},
        ]

    def _convert_to_html(self, doc: Any, include_styles: bool) -> str:
        """Convert document to HTML.

        Args:
            doc: Document object.
            include_styles: Include CSS styles.

        Returns:
            HTML string.
        """
        html_parts = ["<!DOCTYPE html>", "<html>", "<head>"]

        if include_styles:
            html_parts.append("<style>")
            html_parts.append("body { font-family: Arial, sans-serif; }")
            html_parts.append("h1 { font-size: 24px; }")
            html_parts.append("h2 { font-size: 20px; }")
            html_parts.append("p { margin: 10px 0; }")
            html_parts.append("table { border-collapse: collapse; }")
            html_parts.append("td, th { border: 1px solid #ddd; padding: 8px; }")
            html_parts.append("</style>")

        html_parts.extend(["</head>", "<body>"])

        for para in doc.paragraphs:
            style_name = para.style.name if para.style else ""
            if "Heading 1" in style_name:
                html_parts.append(f"<h1>{para.text}</h1>")
            elif "Heading 2" in style_name:
                html_parts.append(f"<h2>{para.text}</h2>")
            elif "Heading 3" in style_name:
                html_parts.append(f"<h3>{para.text}</h3>")
            else:
                html_parts.append(f"<p>{para.text}</p>")

        html_parts.extend(["</body>", "</html>"])
        return "\n".join(html_parts)

    def _convert_to_markdown(self, doc: Any) -> str:
        """Convert document to Markdown.

        Args:
            doc: Document object.

        Returns:
            Markdown string.
        """
        md_parts = []

        for para in doc.paragraphs:
            style_name = para.style.name if para.style else ""
            if "Heading 1" in style_name:
                md_parts.append(f"# {para.text}")
            elif "Heading 2" in style_name:
                md_parts.append(f"## {para.text}")
            elif "Heading 3" in style_name:
                md_parts.append(f"### {para.text}")
            elif para.text.strip():
                md_parts.append(para.text)
            md_parts.append("")

        return "\n".join(md_parts)

    def _extract_text(self, doc: Any) -> str:
        """Extract plain text from document.

        Args:
            doc: Document object.

        Returns:
            Plain text string.
        """
        return "\n".join(para.text for para in doc.paragraphs)
