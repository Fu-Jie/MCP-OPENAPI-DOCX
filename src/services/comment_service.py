"""Comment service for comment operations.

This module provides the CommentService class for managing
document comments and annotations.
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import DocumentProcessingError
from src.handlers.comment_handler import CommentHandler
from src.handlers.document_handler import DocumentHandler


class CommentService:
    """Service class for comment operations.

    Attributes:
        db: Database session.
        document_handler: Handler for document operations.
        comment_handler: Handler for comment operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the comment service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.document_handler = DocumentHandler()
        self.comment_handler = CommentHandler()

    async def add_comment(
        self,
        document_path: str,
        text: str,
        author: str,
        paragraph_index: int | None = None,
        run_start: int | None = None,
        run_end: int | None = None,
    ) -> dict[str, Any]:
        """Add a comment to the document.

        Args:
            document_path: Path to the document.
            text: Comment text.
            author: Comment author.
            paragraph_index: Optional paragraph to comment on.
            run_start: Optional start run index.
            run_end: Optional end run index.

        Returns:
            Result with comment details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            comment_id = self.comment_handler.add_comment(
                doc, text, author, paragraph_index, run_start, run_end
            )
            self.document_handler.save_document(doc, document_path)
            return {
                "success": True,
                "comment_id": comment_id,
                "author": author,
                "text": text,
            }
        except Exception as e:
            raise DocumentProcessingError(f"Failed to add comment: {str(e)}")

    async def get_comments(
        self,
        document_path: str,
    ) -> list[dict[str, Any]]:
        """Get all comments from the document.

        Args:
            document_path: Path to the document.

        Returns:
            List of comments.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.comment_handler.get_comments(doc)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to get comments: {str(e)}")

    async def get_comment(
        self,
        document_path: str,
        comment_id: str,
    ) -> dict[str, Any]:
        """Get a specific comment.

        Args:
            document_path: Path to the document.
            comment_id: Comment ID.

        Returns:
            Comment details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.comment_handler.get_comment(doc, comment_id)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to get comment: {str(e)}")

    async def update_comment(
        self,
        document_path: str,
        comment_id: str,
        text: str,
    ) -> dict[str, Any]:
        """Update a comment.

        Args:
            document_path: Path to the document.
            comment_id: Comment ID.
            text: New comment text.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.comment_handler.update_comment(doc, comment_id, text)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "comment_id": comment_id}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to update comment: {str(e)}")

    async def delete_comment(
        self,
        document_path: str,
        comment_id: str,
    ) -> dict[str, Any]:
        """Delete a comment.

        Args:
            document_path: Path to the document.
            comment_id: Comment ID.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.comment_handler.delete_comment(doc, comment_id)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "deleted": comment_id}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to delete comment: {str(e)}")

    async def reply_to_comment(
        self,
        document_path: str,
        comment_id: str,
        text: str,
        author: str,
    ) -> dict[str, Any]:
        """Reply to a comment.

        Args:
            document_path: Path to the document.
            comment_id: Parent comment ID.
            text: Reply text.
            author: Reply author.

        Returns:
            Result with reply details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            reply_id = self.comment_handler.reply_to_comment(
                doc, comment_id, text, author
            )
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "reply_id": reply_id, "parent_id": comment_id}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to reply to comment: {str(e)}")

    async def resolve_comment(
        self,
        document_path: str,
        comment_id: str,
    ) -> dict[str, Any]:
        """Mark a comment as resolved.

        Args:
            document_path: Path to the document.
            comment_id: Comment ID.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.comment_handler.resolve_comment(doc, comment_id)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "resolved": comment_id}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to resolve comment: {str(e)}")
