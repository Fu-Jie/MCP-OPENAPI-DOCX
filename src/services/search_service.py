"""Search service for search and replace operations.

This module provides the SearchService class for searching
and replacing text in documents.
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import DocumentProcessingError
from src.handlers.document_handler import DocumentHandler
from src.handlers.text_handler import TextHandler


class SearchService:
    """Service class for search operations.

    Attributes:
        db: Database session.
        document_handler: Handler for document operations.
        text_handler: Handler for text operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the search service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.document_handler = DocumentHandler()
        self.text_handler = TextHandler()

    async def search_text(
        self,
        document_path: str,
        query: str,
        case_sensitive: bool = False,
        whole_word: bool = False,
    ) -> list[dict[str, Any]]:
        """Search for text in document.

        Args:
            document_path: Path to the document.
            query: Search query.
            case_sensitive: Match case.
            whole_word: Match whole words only.

        Returns:
            List of search results.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.text_handler.search_text(doc, query, case_sensitive, whole_word)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to search: {str(e)}")

    async def replace_text(
        self,
        document_path: str,
        search: str,
        replace: str,
        case_sensitive: bool = False,
        whole_word: bool = False,
        replace_all: bool = True,
    ) -> dict[str, Any]:
        """Replace text in document.

        Args:
            document_path: Path to the document.
            search: Text to search for.
            replace: Replacement text.
            case_sensitive: Match case.
            whole_word: Match whole words only.
            replace_all: Replace all occurrences.

        Returns:
            Result with replacement count.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            count = self.text_handler.replace_text(
                doc, search, replace, case_sensitive, whole_word, replace_all
            )
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "replaced_count": count}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to replace: {str(e)}")

    async def find_and_highlight(
        self,
        document_path: str,
        query: str,
        color: str = "yellow",
    ) -> dict[str, Any]:
        """Find and highlight text.

        Args:
            document_path: Path to the document.
            query: Search query.
            color: Highlight color.

        Returns:
            Result with highlight count.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            count = self.text_handler.find_and_highlight(doc, query, color)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "highlighted_count": count}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to highlight: {str(e)}")

    async def regex_search(
        self,
        document_path: str,
        pattern: str,
    ) -> list[dict[str, Any]]:
        """Search using regular expression.

        Args:
            document_path: Path to the document.
            pattern: Regular expression pattern.

        Returns:
            List of matches.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.text_handler.regex_search(doc, pattern)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to regex search: {str(e)}")

    async def regex_replace(
        self,
        document_path: str,
        pattern: str,
        replacement: str,
    ) -> dict[str, Any]:
        """Replace using regular expression.

        Args:
            document_path: Path to the document.
            pattern: Regular expression pattern.
            replacement: Replacement string.

        Returns:
            Result with replacement count.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            count = self.text_handler.regex_replace(doc, pattern, replacement)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "replaced_count": count}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to regex replace: {str(e)}")
