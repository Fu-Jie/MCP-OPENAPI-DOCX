"""Revision service for revision tracking operations.

This module provides the RevisionService class for managing
document revisions and track changes.
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import DocumentProcessingError
from src.handlers.document_handler import DocumentHandler
from src.handlers.revision_handler import RevisionHandler


class RevisionService:
    """Service class for revision operations.

    Attributes:
        db: Database session.
        document_handler: Handler for document operations.
        revision_handler: Handler for revision operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the revision service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.document_handler = DocumentHandler()
        self.revision_handler = RevisionHandler()

    async def enable_tracking(
        self,
        document_path: str,
    ) -> dict[str, Any]:
        """Enable revision tracking.

        Args:
            document_path: Path to the document.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.revision_handler.enable_tracking(doc)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "tracking": True}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to enable tracking: {str(e)}")

    async def disable_tracking(
        self,
        document_path: str,
    ) -> dict[str, Any]:
        """Disable revision tracking.

        Args:
            document_path: Path to the document.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.revision_handler.disable_tracking(doc)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "tracking": False}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to disable tracking: {str(e)}")

    async def get_revisions(
        self,
        document_path: str,
    ) -> list[dict[str, Any]]:
        """Get all revisions.

        Args:
            document_path: Path to the document.

        Returns:
            List of revisions.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.revision_handler.get_revisions(doc)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to get revisions: {str(e)}")

    async def accept_revision(
        self,
        document_path: str,
        revision_id: str,
    ) -> dict[str, Any]:
        """Accept a revision.

        Args:
            document_path: Path to the document.
            revision_id: Revision ID.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.revision_handler.accept_revision(doc, revision_id)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "accepted": revision_id}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to accept revision: {str(e)}")

    async def reject_revision(
        self,
        document_path: str,
        revision_id: str,
    ) -> dict[str, Any]:
        """Reject a revision.

        Args:
            document_path: Path to the document.
            revision_id: Revision ID.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.revision_handler.reject_revision(doc, revision_id)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "rejected": revision_id}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to reject revision: {str(e)}")

    async def accept_all_revisions(
        self,
        document_path: str,
    ) -> dict[str, Any]:
        """Accept all revisions.

        Args:
            document_path: Path to the document.

        Returns:
            Result with count of accepted revisions.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            count = self.revision_handler.accept_all_revisions(doc)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "accepted_count": count}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to accept all revisions: {str(e)}")

    async def reject_all_revisions(
        self,
        document_path: str,
    ) -> dict[str, Any]:
        """Reject all revisions.

        Args:
            document_path: Path to the document.

        Returns:
            Result with count of rejected revisions.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            count = self.revision_handler.reject_all_revisions(doc)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "rejected_count": count}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to reject all revisions: {str(e)}")

    async def compare_documents(
        self,
        document_path1: str,
        document_path2: str,
    ) -> dict[str, Any]:
        """Compare two documents.

        Args:
            document_path1: Path to first document.
            document_path2: Path to second document.

        Returns:
            Comparison result with differences.
        """
        try:
            doc1 = self.document_handler.load_document(document_path1)
            doc2 = self.document_handler.load_document(document_path2)
            return self.revision_handler.compare_documents(doc1, doc2)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to compare documents: {str(e)}")
