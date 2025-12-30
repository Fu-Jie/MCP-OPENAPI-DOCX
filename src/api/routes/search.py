"""Search routes.

This module provides endpoints for search operations.
"""

import os
from typing import Any

from fastapi import APIRouter

from src.core.config import get_settings
from src.core.exceptions import DocumentNotFoundError
from src.handlers.document_handler import DocumentHandler
from src.handlers.text_handler import TextHandler
from src.models.schemas import SearchQuery

router = APIRouter(prefix="/documents/{document_id}/search")


def get_search_handler(document_id: str) -> tuple[DocumentHandler, TextHandler]:
    """Get text handler for search operations."""
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    return doc_handler, TextHandler(doc_handler.document)


@router.post(
    "",
    summary="Search Text",
    description="Search for text in the document.",
)
async def search_text(
    document_id: str,
    query: SearchQuery,
) -> dict[str, Any]:
    """Search for text.

    Args:
        document_id: Document UUID.
        query: Search query.

    Returns:
        Search results.
    """
    _, handler = get_search_handler(document_id)
    results = handler.find_text(
        search_text=query.query,
        case_sensitive=query.case_sensitive,
        whole_word=query.whole_word,
    )

    return {
        "document_id": document_id,
        "query": query.query,
        "count": len(results),
        "results": results,
    }


@router.get(
    "/find",
    summary="Quick Find",
    description="Quick text search.",
)
async def quick_find(
    document_id: str,
    q: str,
    case_sensitive: bool = False,
    whole_word: bool = False,
) -> dict[str, Any]:
    """Quick search.

    Args:
        document_id: Document UUID.
        q: Search query.
        case_sensitive: Case-sensitive search.
        whole_word: Match whole words only.

    Returns:
        Search results.
    """
    _, handler = get_search_handler(document_id)
    results = handler.find_text(
        search_text=q,
        case_sensitive=case_sensitive,
        whole_word=whole_word,
    )

    return {
        "query": q,
        "count": len(results),
        "results": results,
    }
