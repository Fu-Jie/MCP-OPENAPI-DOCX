"""TOC and navigation routes.

This module provides endpoints for table of contents, bookmarks, and hyperlinks.
"""

import os
from typing import Any

from fastapi import APIRouter

from src.core.config import get_settings
from src.core.exceptions import DocumentNotFoundError
from src.handlers.document_handler import DocumentHandler
from src.handlers.toc_handler import TocHandler
from src.models.schemas import BookmarkCreate, HyperlinkCreate, TocCreate

router = APIRouter(prefix="/documents/{document_id}/toc")


def get_toc_handler(document_id: str) -> tuple[DocumentHandler, TocHandler]:
    """Get TOC handler for a document."""
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    return doc_handler, TocHandler(doc_handler.document)


@router.post(
    "",
    summary="Add Table of Contents",
    description="Add a table of contents to the document.",
)
async def add_toc(
    document_id: str,
    data: TocCreate,
) -> dict[str, Any]:
    """Add a table of contents.

    Args:
        document_id: Document UUID.
        data: TOC creation data.

    Returns:
        Created TOC information.
    """
    doc_handler, handler = get_toc_handler(document_id)
    index = handler.add_table_of_contents(
        title=data.title,
        max_level=data.max_level,
        paragraph_index=data.paragraph_index,
    )
    doc_handler.save_document()

    return {
        "index": index,
        "title": data.title,
        "max_level": data.max_level,
    }


@router.get(
    "/headings",
    summary="Get Headings",
    description="Get all headings in the document.",
)
async def get_headings(document_id: str) -> dict[str, Any]:
    """Get all headings.

    Args:
        document_id: Document UUID.

    Returns:
        List of headings.
    """
    _, handler = get_toc_handler(document_id)
    headings = handler.get_headings()

    return {
        "document_id": document_id,
        "count": len(headings),
        "headings": headings,
    }


@router.post(
    "/headings",
    summary="Add Heading",
    description="Add a heading to the document.",
)
async def add_heading(
    document_id: str,
    text: str,
    level: int = 1,
) -> dict[str, Any]:
    """Add a heading.

    Args:
        document_id: Document UUID.
        text: Heading text.
        level: Heading level (1-9).

    Returns:
        Created heading information.
    """
    doc_handler, handler = get_toc_handler(document_id)
    index = handler.add_heading(text, level)
    doc_handler.save_document()

    return {
        "index": index,
        "text": text,
        "level": level,
    }


@router.get(
    "/bookmarks",
    summary="Get Bookmarks",
    description="Get all bookmarks in the document.",
)
async def get_bookmarks(document_id: str) -> dict[str, Any]:
    """Get all bookmarks.

    Args:
        document_id: Document UUID.

    Returns:
        List of bookmarks.
    """
    _, handler = get_toc_handler(document_id)
    bookmarks = handler.get_bookmarks()

    return {
        "document_id": document_id,
        "count": len(bookmarks),
        "bookmarks": [
            {"name": b.name, "paragraph_index": b.paragraph_index} for b in bookmarks
        ],
    }


@router.post(
    "/bookmarks",
    summary="Add Bookmark",
    description="Add a bookmark to the document.",
)
async def add_bookmark(
    document_id: str,
    data: BookmarkCreate,
) -> dict[str, Any]:
    """Add a bookmark.

    Args:
        document_id: Document UUID.
        data: Bookmark creation data.

    Returns:
        Created bookmark information.
    """
    doc_handler, handler = get_toc_handler(document_id)
    bookmark = handler.add_bookmark(data.name, data.paragraph_index)
    doc_handler.save_document()

    return {
        "name": bookmark.name,
        "paragraph_index": bookmark.paragraph_index,
    }


@router.delete(
    "/bookmarks/{name}",
    summary="Delete Bookmark",
    description="Delete a bookmark from the document.",
)
async def delete_bookmark(
    document_id: str,
    name: str,
) -> dict[str, Any]:
    """Delete a bookmark.

    Args:
        document_id: Document UUID.
        name: Bookmark name.

    Returns:
        Deletion confirmation.
    """
    doc_handler, handler = get_toc_handler(document_id)
    handler.delete_bookmark(name)
    doc_handler.save_document()

    return {"deleted": True, "name": name}


@router.get(
    "/hyperlinks",
    summary="Get Hyperlinks",
    description="Get all hyperlinks in the document.",
)
async def get_hyperlinks(document_id: str) -> dict[str, Any]:
    """Get all hyperlinks.

    Args:
        document_id: Document UUID.

    Returns:
        List of hyperlinks.
    """
    _, handler = get_toc_handler(document_id)
    hyperlinks = handler.get_hyperlinks()

    return {
        "document_id": document_id,
        "count": len(hyperlinks),
        "hyperlinks": [
            {
                "text": h.text,
                "url": h.url,
                "paragraph_index": h.paragraph_index,
            }
            for h in hyperlinks
        ],
    }


@router.post(
    "/hyperlinks",
    summary="Add Hyperlink",
    description="Add a hyperlink to the document.",
)
async def add_hyperlink(
    document_id: str,
    data: HyperlinkCreate,
) -> dict[str, Any]:
    """Add a hyperlink.

    Args:
        document_id: Document UUID.
        data: Hyperlink creation data.

    Returns:
        Created hyperlink information.
    """
    doc_handler, handler = get_toc_handler(document_id)
    hyperlink = handler.add_hyperlink(
        text=data.text,
        url=data.url,
        paragraph_index=data.paragraph_index,
        offset=data.offset,
    )
    doc_handler.save_document()

    return {
        "text": hyperlink.text,
        "url": hyperlink.url,
        "paragraph_index": hyperlink.paragraph_index,
    }


@router.post(
    "/internal-links",
    summary="Add Internal Link",
    description="Add an internal link to a bookmark.",
)
async def add_internal_link(
    document_id: str,
    text: str,
    bookmark_name: str,
    paragraph_index: int,
) -> dict[str, Any]:
    """Add an internal link.

    Args:
        document_id: Document UUID.
        text: Link text.
        bookmark_name: Target bookmark name.
        paragraph_index: Paragraph index.

    Returns:
        Created link information.
    """
    doc_handler, handler = get_toc_handler(document_id)
    hyperlink = handler.add_internal_link(text, bookmark_name, paragraph_index)
    doc_handler.save_document()

    return {
        "text": hyperlink.text,
        "bookmark": bookmark_name,
        "paragraph_index": hyperlink.paragraph_index,
    }
