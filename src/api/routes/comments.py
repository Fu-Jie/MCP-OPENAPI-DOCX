"""Comment routes.

This module provides endpoints for comment operations.
"""

import os
from typing import Any

from fastapi import APIRouter

from src.core.config import get_settings
from src.core.enums import CommentStatus
from src.core.exceptions import DocumentNotFoundError
from src.handlers.document_handler import DocumentHandler
from src.handlers.comment_handler import CommentHandler
from src.models.schemas import CommentCreate, CommentUpdate

router = APIRouter(prefix="/documents/{document_id}/comments")

# Store handlers per document session (simplified)
_comment_handlers: dict[str, CommentHandler] = {}


def get_comment_handler(document_id: str) -> tuple[DocumentHandler, CommentHandler]:
    """Get comment handler for a document."""
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)

    if document_id not in _comment_handlers:
        _comment_handlers[document_id] = CommentHandler(doc_handler.document)

    return doc_handler, _comment_handlers[document_id]


@router.get(
    "",
    summary="Get All Comments",
    description="Get all comments in the document.",
)
async def get_comments(document_id: str) -> dict[str, Any]:
    """Get all comments.

    Args:
        document_id: Document UUID.

    Returns:
        List of comments.
    """
    _, handler = get_comment_handler(document_id)
    comments = handler.get_all_comments()

    return {
        "document_id": document_id,
        "count": len(comments),
        "comments": handler.export_comments(),
    }


@router.get(
    "/stats",
    summary="Get Comment Statistics",
    description="Get comment count statistics.",
)
async def get_comment_stats(document_id: str) -> dict[str, Any]:
    """Get comment statistics.

    Args:
        document_id: Document UUID.

    Returns:
        Comment statistics.
    """
    _, handler = get_comment_handler(document_id)
    return handler.get_comment_count()


@router.get(
    "/{comment_id}",
    summary="Get Comment",
    description="Get a specific comment by ID.",
)
async def get_comment(
    document_id: str,
    comment_id: int,
) -> dict[str, Any]:
    """Get a comment.

    Args:
        document_id: Document UUID.
        comment_id: Comment ID.

    Returns:
        Comment information.
    """
    _, handler = get_comment_handler(document_id)
    return handler.get_comment(comment_id)


@router.post(
    "",
    summary="Add Comment",
    description="Add a comment to the document.",
)
async def add_comment(
    document_id: str,
    data: CommentCreate,
    author: str = "User",
) -> dict[str, Any]:
    """Add a comment.

    Args:
        document_id: Document UUID.
        data: Comment creation data.
        author: Author name.

    Returns:
        Created comment information.
    """
    doc_handler, handler = get_comment_handler(document_id)
    comment = handler.add_comment(
        text=data.content,
        author=author,
        paragraph_index=data.paragraph_index or 0,
        start_offset=data.start_offset,
        end_offset=data.end_offset,
    )
    doc_handler.save_document()

    return comment


@router.put(
    "/{comment_id}",
    summary="Update Comment",
    description="Update a comment.",
)
async def update_comment(
    document_id: str,
    comment_id: int,
    data: CommentUpdate,
) -> dict[str, Any]:
    """Update a comment.

    Args:
        document_id: Document UUID.
        comment_id: Comment ID.
        data: Update data.

    Returns:
        Updated comment information.
    """
    doc_handler, handler = get_comment_handler(document_id)
    comment = handler.update_comment(
        comment_id=comment_id,
        text=data.content,
        status=data.status,
    )
    doc_handler.save_document()

    return comment


@router.delete(
    "/{comment_id}",
    summary="Delete Comment",
    description="Delete a comment.",
)
async def delete_comment(
    document_id: str,
    comment_id: int,
) -> dict[str, Any]:
    """Delete a comment.

    Args:
        document_id: Document UUID.
        comment_id: Comment ID.

    Returns:
        Deletion confirmation.
    """
    doc_handler, handler = get_comment_handler(document_id)
    handler.delete_comment(comment_id)
    doc_handler.save_document()

    return {"deleted": True, "comment_id": comment_id}


@router.post(
    "/{comment_id}/resolve",
    summary="Resolve Comment",
    description="Mark a comment as resolved.",
)
async def resolve_comment(
    document_id: str,
    comment_id: int,
) -> dict[str, Any]:
    """Resolve a comment.

    Args:
        document_id: Document UUID.
        comment_id: Comment ID.

    Returns:
        Updated comment information.
    """
    doc_handler, handler = get_comment_handler(document_id)
    comment = handler.resolve_comment(comment_id)
    doc_handler.save_document()

    return comment


@router.post(
    "/{comment_id}/reopen",
    summary="Reopen Comment",
    description="Reopen a resolved comment.",
)
async def reopen_comment(
    document_id: str,
    comment_id: int,
) -> dict[str, Any]:
    """Reopen a comment.

    Args:
        document_id: Document UUID.
        comment_id: Comment ID.

    Returns:
        Updated comment information.
    """
    doc_handler, handler = get_comment_handler(document_id)
    comment = handler.reopen_comment(comment_id)
    doc_handler.save_document()

    return comment


@router.post(
    "/{comment_id}/replies",
    summary="Add Reply",
    description="Add a reply to a comment.",
)
async def add_reply(
    document_id: str,
    comment_id: int,
    text: str,
    author: str = "User",
) -> dict[str, Any]:
    """Add a reply to a comment.

    Args:
        document_id: Document UUID.
        comment_id: Comment ID.
        text: Reply text.
        author: Author name.

    Returns:
        Created reply information.
    """
    doc_handler, handler = get_comment_handler(document_id)
    reply = handler.add_reply(comment_id, text, author)
    doc_handler.save_document()

    return reply


@router.get(
    "/paragraph/{paragraph_index}",
    summary="Get Paragraph Comments",
    description="Get all comments for a specific paragraph.",
)
async def get_paragraph_comments(
    document_id: str,
    paragraph_index: int,
) -> dict[str, Any]:
    """Get comments for a paragraph.

    Args:
        document_id: Document UUID.
        paragraph_index: Paragraph index.

    Returns:
        List of comments.
    """
    _, handler = get_comment_handler(document_id)
    comments = handler.get_paragraph_comments(paragraph_index)

    return {
        "paragraph_index": paragraph_index,
        "count": len(comments),
        "comments": comments,
    }
