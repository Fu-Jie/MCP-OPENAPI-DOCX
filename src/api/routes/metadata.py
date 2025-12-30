"""Metadata routes.

This module provides endpoints for document metadata operations.
"""

import os
from typing import Any

from fastapi import APIRouter

from src.core.config import get_settings
from src.core.exceptions import DocumentNotFoundError
from src.handlers.document_handler import DocumentHandler

router = APIRouter(prefix="/documents/{document_id}/metadata")


@router.get(
    "",
    summary="Get Metadata",
    description="Get document metadata.",
)
async def get_metadata(document_id: str) -> dict[str, Any]:
    """Get document metadata.

    Args:
        document_id: Document UUID.

    Returns:
        Document metadata.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    handler = DocumentHandler()
    handler.open_document(file_path)
    metadata = handler.get_metadata()

    return {
        "author": metadata.author,
        "title": metadata.title,
        "subject": metadata.subject,
        "keywords": metadata.keywords,
        "comments": metadata.comments,
        "category": metadata.category,
        "created": metadata.created.isoformat() if metadata.created else None,
        "modified": metadata.modified.isoformat() if metadata.modified else None,
        "last_modified_by": metadata.last_modified_by,
        "revision": metadata.revision,
    }


@router.put(
    "",
    summary="Update Metadata",
    description="Update document metadata.",
)
async def update_metadata(
    document_id: str,
    author: str | None = None,
    title: str | None = None,
    subject: str | None = None,
    keywords: str | None = None,
    comments: str | None = None,
    category: str | None = None,
) -> dict[str, Any]:
    """Update document metadata.

    Args:
        document_id: Document UUID.
        author: Document author.
        title: Document title.
        subject: Document subject.
        keywords: Document keywords.
        comments: Document comments.
        category: Document category.

    Returns:
        Updated metadata.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    handler = DocumentHandler()
    handler.open_document(file_path)
    handler.set_metadata(
        author=author,
        title=title,
        subject=subject,
        keywords=keywords,
        comments=comments,
        category=category,
    )
    handler.save_document()

    return {
        "updated": True,
        "author": author,
        "title": title,
        "subject": subject,
        "keywords": keywords,
        "comments": comments,
        "category": category,
    }


@router.get(
    "/statistics",
    summary="Get Statistics",
    description="Get document statistics.",
)
async def get_statistics(document_id: str) -> dict[str, Any]:
    """Get document statistics.

    Args:
        document_id: Document UUID.

    Returns:
        Document statistics.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    handler = DocumentHandler()
    handler.open_document(file_path)
    structure = handler.get_document_structure()

    return {
        "paragraphs": structure["paragraphs"],
        "tables": structure["tables"],
        "sections": structure["sections"],
        "styles": structure["styles"],
        "images": structure["inline_shapes"],
        "word_count": handler.get_word_count(),
        "character_count": handler.get_character_count(),
        "character_count_no_spaces": handler.get_character_count(include_spaces=False),
    }


@router.get(
    "/structure",
    summary="Get Structure",
    description="Get document structure.",
)
async def get_structure(document_id: str) -> dict[str, Any]:
    """Get document structure.

    Args:
        document_id: Document UUID.

    Returns:
        Document structure.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    handler = DocumentHandler()
    handler.open_document(file_path)

    return handler.get_document_structure()
