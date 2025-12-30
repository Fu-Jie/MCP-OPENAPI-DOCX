"""Comment handler for document comment operations.

This module provides functionality for managing comments
and annotations in DOCX documents.
"""

from datetime import datetime
from typing import Any

from docx import Document

from src.core.enums import CommentStatus
from src.core.exceptions import ValidationError


class CommentHandler:
    """Handler for comment operations.

    This class provides methods for managing comments
    in DOCX documents.
    """

    def __init__(self, document: Document) -> None:
        """Initialize the comment handler.

        Args:
            document: The Document instance to work with.
        """
        self._document = document
        self._comments: list[dict[str, Any]] = []
        self._next_id = 0

    @property
    def document(self) -> Document:
        """Get the document instance."""
        return self._document

    def add_comment(
        self,
        text: str,
        author: str,
        paragraph_index: int,
        start_offset: int | None = None,
        end_offset: int | None = None,
    ) -> dict[str, Any]:
        """Add a comment to the document.

        Args:
            text: Comment text content.
            author: Author name.
            paragraph_index: Index of the paragraph to comment on.
            start_offset: Optional start character offset.
            end_offset: Optional end character offset.

        Returns:
            Comment information dictionary.

        Raises:
            ValidationError: If the paragraph index is out of range.

        Note:
            Full comment support requires complex XML manipulation.
            This is a simplified implementation.
        """
        if paragraph_index < 0 or paragraph_index >= len(self._document.paragraphs):
            raise ValidationError(f"Paragraph index {paragraph_index} out of range")

        comment_id = self._next_id
        self._next_id += 1

        comment = {
            "id": comment_id,
            "text": text,
            "author": author,
            "paragraph_index": paragraph_index,
            "start_offset": start_offset,
            "end_offset": end_offset,
            "status": CommentStatus.OPEN,
            "created_at": datetime.now(),
            "replies": [],
        }

        self._comments.append(comment)

        # Note: Adding actual XML comments to DOCX requires manipulating
        # the comments.xml part which is complex. This is a simplified version.

        return comment

    def get_comment(self, comment_id: int) -> dict[str, Any]:
        """Get a comment by ID.

        Args:
            comment_id: Comment ID.

        Returns:
            Comment information dictionary.

        Raises:
            ValidationError: If the comment is not found.
        """
        for comment in self._comments:
            if comment["id"] == comment_id:
                return comment

        raise ValidationError(f"Comment not found: {comment_id}")

    def get_all_comments(self) -> list[dict[str, Any]]:
        """Get all comments in the document.

        Returns:
            List of comment dictionaries.
        """
        return self._comments.copy()

    def get_paragraph_comments(
        self,
        paragraph_index: int,
    ) -> list[dict[str, Any]]:
        """Get all comments for a specific paragraph.

        Args:
            paragraph_index: Index of the paragraph.

        Returns:
            List of comments for the paragraph.

        Raises:
            ValidationError: If the index is out of range.
        """
        if paragraph_index < 0 or paragraph_index >= len(self._document.paragraphs):
            raise ValidationError(f"Paragraph index {paragraph_index} out of range")

        return [c for c in self._comments if c["paragraph_index"] == paragraph_index]

    def update_comment(
        self,
        comment_id: int,
        text: str | None = None,
        status: CommentStatus | None = None,
    ) -> dict[str, Any]:
        """Update a comment.

        Args:
            comment_id: Comment ID.
            text: New comment text.
            status: New comment status.

        Returns:
            Updated comment dictionary.

        Raises:
            ValidationError: If the comment is not found.
        """
        for comment in self._comments:
            if comment["id"] == comment_id:
                if text is not None:
                    comment["text"] = text
                if status is not None:
                    comment["status"] = status
                return comment

        raise ValidationError(f"Comment not found: {comment_id}")

    def delete_comment(self, comment_id: int) -> None:
        """Delete a comment.

        Args:
            comment_id: Comment ID.

        Raises:
            ValidationError: If the comment is not found.
        """
        for i, comment in enumerate(self._comments):
            if comment["id"] == comment_id:
                self._comments.pop(i)
                return

        raise ValidationError(f"Comment not found: {comment_id}")

    def resolve_comment(self, comment_id: int) -> dict[str, Any]:
        """Mark a comment as resolved.

        Args:
            comment_id: Comment ID.

        Returns:
            Updated comment dictionary.

        Raises:
            ValidationError: If the comment is not found.
        """
        return self.update_comment(comment_id, status=CommentStatus.RESOLVED)

    def reopen_comment(self, comment_id: int) -> dict[str, Any]:
        """Reopen a resolved comment.

        Args:
            comment_id: Comment ID.

        Returns:
            Updated comment dictionary.

        Raises:
            ValidationError: If the comment is not found.
        """
        return self.update_comment(comment_id, status=CommentStatus.OPEN)

    def add_reply(
        self,
        comment_id: int,
        text: str,
        author: str,
    ) -> dict[str, Any]:
        """Add a reply to a comment.

        Args:
            comment_id: Parent comment ID.
            text: Reply text.
            author: Reply author.

        Returns:
            The reply dictionary.

        Raises:
            ValidationError: If the parent comment is not found.
        """
        parent = self.get_comment(comment_id)

        reply = {
            "id": self._next_id,
            "text": text,
            "author": author,
            "created_at": datetime.now(),
        }
        self._next_id += 1

        parent["replies"].append(reply)
        return reply

    def get_open_comments(self) -> list[dict[str, Any]]:
        """Get all open (unresolved) comments.

        Returns:
            List of open comments.
        """
        return [c for c in self._comments if c["status"] == CommentStatus.OPEN]

    def get_resolved_comments(self) -> list[dict[str, Any]]:
        """Get all resolved comments.

        Returns:
            List of resolved comments.
        """
        return [c for c in self._comments if c["status"] == CommentStatus.RESOLVED]

    def get_comments_by_author(self, author: str) -> list[dict[str, Any]]:
        """Get all comments by a specific author.

        Args:
            author: Author name.

        Returns:
            List of comments by the author.
        """
        return [c for c in self._comments if c["author"] == author]

    def get_comment_count(self) -> dict[str, int]:
        """Get comment statistics.

        Returns:
            Dictionary with comment counts.
        """
        open_count = len(self.get_open_comments())
        resolved_count = len(self.get_resolved_comments())

        return {
            "total": len(self._comments),
            "open": open_count,
            "resolved": resolved_count,
        }

    def clear_all_comments(self) -> int:
        """Remove all comments from the document.

        Returns:
            Number of comments removed.
        """
        count = len(self._comments)
        self._comments.clear()
        return count

    def export_comments(self) -> list[dict[str, Any]]:
        """Export all comments for external processing.

        Returns:
            List of comment dictionaries with all details.
        """
        exported = []
        for comment in self._comments:
            exported.append(
                {
                    "id": comment["id"],
                    "text": comment["text"],
                    "author": comment["author"],
                    "paragraph_index": comment["paragraph_index"],
                    "status": (
                        comment["status"].value
                        if isinstance(comment["status"], CommentStatus)
                        else comment["status"]
                    ),
                    "created_at": comment["created_at"].isoformat(),
                    "replies": [
                        {
                            "id": r["id"],
                            "text": r["text"],
                            "author": r["author"],
                            "created_at": r["created_at"].isoformat(),
                        }
                        for r in comment.get("replies", [])
                    ],
                }
            )
        return exported
